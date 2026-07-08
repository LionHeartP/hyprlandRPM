#!/usr/bin/bash
set -euxo pipefail

SPEC_FILE="noctalia-git.spec"
REPO="noctalia-dev/noctalia"
BRANCH="main"
ec=0

oldCommit="$(grep "%global commit " "$SPEC_FILE" | awk '{print $3}')"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/$REPO/commits/$BRANCH")"

oldVersion="$(rpmspec -q --qf "%{version}\n" "$SPEC_FILE" | head -1)"
oldVersionBase="$(echo "$oldVersion" | sed 's/\^.*//')"
newTag="$(curl -s "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed -e 's/^v//' -e 's/-/~/g' -e 's/null//')"
if [ -z "$newTag" ]; then
    newTag="$oldVersionBase"
fi

rpmdev-vercmp "$oldVersion" "$newTag" || ec=$?

if [ "$oldCommit" == "$newCommit" ] && [ "$ec" -ne 12 ]; then
    echo "No changes detected in commit or version tag."
    exit 0
fi

if [ "$ec" -eq 12 ]; then
    echo "Newer tag detected: $newTag. Resetting snapshot counter."
    sed -i "s/^Version:.*/Version:	$newTag^1.%{shortcommit}/" "$SPEC_FILE"
else
    echo "Same version base, upgrading snapshot counter."
    perl -pe '/^Version:/ && s/\^(\d+)/"^" . ($1 + 1)/e' -i "$SPEC_FILE"
fi

sed -i "s/^%global commit.*/%global commit          $newCommit/" "$SPEC_FILE"

git diff --quiet "$SPEC_FILE" || \
{
    git commit -am "up rev noctalia-git-${newTag:-$oldVersionBase}+${newCommit:0:7}"
    git push
}
