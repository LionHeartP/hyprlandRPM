#!/usr/bin/env bash
set -euo pipefail

SPEC_FILE="hyprmod.spec"

# List of PyPI packages matching Source1 through Source5 order
PACKAGES=(
    "hyprland-config"   # Source1
    "hyprland-monitors" # Source2
    "hyprland-schema"   # Source3
    "hyprland-socket"   # Source4
    "hyprland-state"    # Source5
)

echo "==> Cleaning up old wheel files..."
rm -f hyprland_*.whl

echo "==> Downloading latest wheels from PyPI..."
pip download "${PACKAGES[@]}" -d . --no-deps

echo "==> Updating $SPEC_FILE..."
i=1
for pkg in "${PACKAGES[@]}"; do
    # PyPI wheel filenames convert hyphens to underscores
    pkg_norm=$(echo "$pkg" | tr '-' '_')

    # Find the newly downloaded wheel file
    whl_file=$(ls -1 ${pkg_norm}-*.whl 2>/dev/null | head -n1)

    if [ -n "$whl_file" ]; then
        whl_name=$(basename "$whl_file")
        echo "Setting Source${i}: ${whl_name}"

        # Replace the SourceX line in the spec file
        sed -i -E "s/^(Source${i}:[[:space:]]+).*/\1${whl_name}/" "$SPEC_FILE"
    else
        echo "Error: Wheel for $pkg was not found!" >&2
        exit 1
    fi
    ((i++))
done

echo "==> Successfully updated $SPEC_FILE!"
