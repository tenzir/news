#!/usr/bin/env bash
# Synchronize package changelogs from a package library.
#
# Usage: sync-packages.sh <source_dir> <target_dir>
#
# A package is a top-level directory of the source with a `package.yaml` and a
# `changelog/` directory. This copies both to `<target_dir>/<package>/`, where
# tenzir-ship reads them in package mode, and removes packages from the target
# that no longer exist in the source.

set -euo pipefail

source_dir="$1"
target_dir="$2"

synced=0
for manifest in "$source_dir"/*/package.yaml; do
  package_dir="${manifest%/package.yaml}"
  [[ -f "$manifest" && -d "$package_dir/changelog" ]] || continue
  package="${package_dir##*/}"
  mkdir -p "$target_dir/$package/changelog"
  cp "$manifest" "$target_dir/$package/package.yaml"
  rsync -a --delete "$package_dir/changelog/" "$target_dir/$package/changelog/"
  synced=$((synced + 1))
done

# Refuse to continue without packages: removing orphans would otherwise wipe
# the whole target after a wrong source path.
if ((synced == 0)); then
  echo "::error::No packages with package.yaml and changelog/ in $source_dir"
  exit 1
fi
echo "Synchronized $synced package changelogs"

for dest in "$target_dir"/*/; do
  package="$(basename "$dest")"
  if [[ ! -f "$source_dir/$package/package.yaml" ||
        ! -d "$source_dir/$package/changelog" ]]; then
    echo "Removing orphaned package: $target_dir/$package"
    rm -rf "$dest"
  fi
done
