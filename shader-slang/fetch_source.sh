#!/usr/bin/env bash
set -euo pipefail

SPEC_FILE="${1:-}"

if [[ -z "$SPEC_FILE" ]]; then
    echo "Usage: $0 <path-to-spec-file>"
    exit 1
fi

if [[ ! -f "$SPEC_FILE" ]]; then
    echo "Error: Spec file '$SPEC_FILE' does not exist."
    exit 1
fi

# Extract version using rpmspec if available (handles macros), fallback to grep
if command -v rpmspec &>/dev/null; then
    VERSION=$(rpmspec -q --qf "%{VERSION}\n" "$SPEC_FILE" 2>/dev/null | head -n1)
else
    VERSION=$(grep -i '^\s*Version:' "$SPEC_FILE" | awk '{print $2}')
fi

if [[ -z "$VERSION" ]]; then
    echo "Error: Could not extract Version from '$SPEC_FILE'."
    exit 1
fi

TARBALL="slang-${VERSION}-full.tar.gz"
CLONE_DIR="slang-${VERSION}"

echo "==> Detected Slang Version: ${VERSION}"

if [[ -f "$TARBALL" ]]; then
    echo "==> Output tarball '${TARBALL}' already exists. Skipping."
    exit 0
fi

echo "==> Fetching source repository and submodules for tag v${VERSION}..."
rm -rf "$CLONE_DIR"
git clone --depth 1 --recursive --branch "v${VERSION}" https://github.com/shader-slang/slang.git "$CLONE_DIR"

echo "==> Creating tarball '${TARBALL}'..."
tar --exclude-vcs -czf "$TARBALL" "$CLONE_DIR"

echo "==> Cleaning up temporary directory..."
rm -rf "$CLONE_DIR"

echo "==> Successfully created ${TARBALL}"
