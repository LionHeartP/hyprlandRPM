#!/usr/bin/bash
set -euxo pipefail

SPEC_FILE="quickshell.spec"
REPO="quickshell-mirror/quickshell"
BRANCH="master"
ec=0

oldVersion="$(rpmspec -q --qf "%{version}\n" "$SPEC_FILE" | head -1)"
oldCommit="$(grep "%global commit " "$SPEC_FILE" | awk '{print $3}')"

newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/$REPO/commits/$BRANCH")"
newTag="$(curl -s "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')"

rpmdev-vercmp "$oldVersion" "$newTag" || ec=$?

if [ "$oldCommit" == "$newCommit" ] && [ "$ec" -ne 12 ]; then
    echo "Quickshell is already up to date."
    exit 0
fi

newTimestamp="$(date +"%Y%m%d")"

if [ "$ec" -eq 12 ]; then
    echo "New version detected: $newTag. Resetting release counter."
    sed -i "s/^Version:.*/Version:            $newTag/" "$SPEC_FILE"
    sed -i "s/^\(%global rel_build \)[0-9]*/\11/" "$SPEC_FILE"
else
    echo "Bumping release counter for new commit."
    perl -pe 's/(?<=%global rel_build )(\d+)/$1 + 1/e' -i "$SPEC_FILE"
fi

sed -i "s/^%global commit.*/%global commit $newCommit/" "$SPEC_FILE"
sed -i "s/^%global build_timestamp.*/%global build_timestamp %(date +\"$newTimestamp\")/" "$SPEC_FILE"

git diff --quiet "$SPEC_FILE" || \
{
    git commit -am "up rev quickshell-${newTag:-$oldVersion}+${newCommit:0:7}"
    git push
}
