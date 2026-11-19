#!/usr/bin/env bash
# List the release directories that warrant a release notification.
#
# Usage: list-releases.sh <target_dir> <packages>
#
# For a project, these are its top-level releases, not module releases. For a
# package library (`packages` is `true`), these are the releases of every
# package. The output is sorted, one directory per line.

set -euo pipefail

target_dir="$1"
packages="$2"

if [[ "$packages" == "true" ]]; then
  find "$target_dir" -mindepth 4 -maxdepth 4 -type d \
    -path "$target_dir/*/changelog/releases/*" 2>/dev/null | sort || true
else
  find "$target_dir/changelog/releases" -mindepth 1 -maxdepth 1 -type d \
    2>/dev/null | sort || true
fi
