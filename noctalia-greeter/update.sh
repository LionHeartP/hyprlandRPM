#!/usr/bin/bash
set -euxo pipefail

SPEC_FILE="noctalia-greeter.spec"
REPO="noctalia-dev/noctalia-greeter"
BRANCH="main"
ec=0

oldCommit="$(grep "%global commit " "$SPEC_FILE" | awk '{print $3}')"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/$REPO/commits/$BRANCH")"

oldVersion="$(rpmspec -q --qf "%{version}\n" "$SPEC_FILE" | head -1)"
newTag="$(curl -s "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')"

rpmdev-vercmp "$oldVersion" "$newTag" || ec=$?

if [ "$oldCommit" == "$newCommit" ] && [ "$ec" -ne 12 ]; then
    echo "No changes detected in commit or version tag."
    exit 0
fi

if [ "$ec" -eq 12 ]; then
    echo "Newer tag detected: $newTag. Resetting release bump."
    sed -i "s/^Version:.*/Version:	$newTag/" "$SPEC_FILE"
    sed -i "s/^Release:.*/Release:	1.git%{shortcommit}%{?dist}/" "$SPEC_FILE"
else
    perl -pe 's/(?<=Release:[\t ]*)(\d+)(?=\.git)/$1 + 1/e' -i "$SPEC_FILE"
fi

newTimestamp="$(date +"%Y%m%d")"
sed -i "s/^%global commit.*/%global commit          $newCommit/" "$SPEC_FILE"

git diff --quiet "$SPEC_FILE" || \
{
    git commit -am "up rev noctalia-greeter-${newTag:-$oldVersion}+${newCommit:0:7}"
    git push
}
