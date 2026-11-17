#!/usr/bin/env bash
set -euo pipefail

SPEC_FILE="${1:-luciole-git.spec}"
REPO="noctalia-dev/luciole"
BRANCH="main"
API_URL="https://api.github.com/repos/${REPO}"

if [[ ! -f "${SPEC_FILE}" ]]; then
    printf 'Error: spec file not found: %s\n' "${SPEC_FILE}" >&2
    exit 1
fi

for command in curl jq git awk; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        printf 'Error: required command not found: %s\n' "${command}" >&2
        exit 1
    fi
done

oldCommit="$(awk '$1 == "%global" && $2 == "commit" { print $3; exit }' "${SPEC_FILE}")"
oldVersion="$(awk '$1 == "Version:" { print $2; exit }' "${SPEC_FILE}")"

if [[ -z "${oldCommit}" || -z "${oldVersion}" ]]; then
    echo "Error: could not read %global commit or Version from ${SPEC_FILE}" >&2
    exit 1
fi

curl_args=(--fail --silent --show-error --location
    -H 'Accept: application/vnd.github+json'
    -H 'X-GitHub-Api-Version: 2022-11-28')
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    curl_args+=(-H "Authorization: Bearer ${GITHUB_TOKEN}")
fi

newCommit="$(curl "${curl_args[@]}" "${API_URL}/commits/${BRANCH}" | jq -er '.sha')"
newVersion="$(curl --fail --silent --show-error --location \
    "https://raw.githubusercontent.com/${REPO}/${newCommit}/VERSION" | tr -d '[:space:]')"

if [[ ! "${newCommit}" =~ ^[0-9a-f]{40}$ ]]; then
    printf 'Error: GitHub returned an invalid commit SHA: %s\n' "${newCommit}" >&2
    exit 1
fi
if [[ ! "${newVersion}" =~ ^[0-9A-Za-z.+~_-]+$ ]]; then
    printf 'Error: upstream VERSION has an unexpected value: %s\n' "${newVersion}" >&2
    exit 1
fi

oldVersionBase="${oldVersion%%^*}"
oldSnapshot=0
if [[ "${oldVersion}" =~ \^([0-9]+)\. ]]; then
    oldSnapshot="${BASH_REMATCH[1]}"
fi

if [[ "${oldCommit}" == "${newCommit}" && "${oldVersionBase}" == "${newVersion}" ]]; then
    echo "No changes detected in the upstream commit or VERSION."
    exit 0
fi

if [[ "${oldVersionBase}" == "${newVersion}" ]]; then
    newSnapshot=$((oldSnapshot + 1))
    echo "New main-branch snapshot; incrementing snapshot counter to ${newSnapshot}."
else
    newSnapshot=1
    printf 'Upstream VERSION changed from %s to %s; resetting snapshot counter.\n' \
        "${oldVersionBase}" "${newVersion}"
fi

newRpmVersion="${newVersion}^${newSnapshot}.%{shortcommit}"
tmpFile="$(mktemp)"
trap 'rm -f "${tmpFile}"' EXIT

awk -v version="${newRpmVersion}" -v commit="${newCommit}" '
    $1 == "Version:" { $0 = "Version:\t" version }
    $1 == "Release:" { $0 = "Release:\t1%{?dist}" }
    $1 == "%global" && $2 == "commit" { $0 = "%global commit          " commit }
    { print }
' "${SPEC_FILE}" > "${tmpFile}"
cat "${tmpFile}" > "${SPEC_FILE}"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git add -- "${SPEC_FILE}"
    if ! git diff --cached --quiet -- "${SPEC_FILE}"; then
        git commit -m "chore: update luciole-git to ${newVersion}^${newSnapshot}+${newCommit:0:7}"
        git push origin "HEAD:refs/heads/${BRANCH}"
    fi
else
    echo "Updated ${SPEC_FILE}; not committing because this is not a Git worktree."
fi
