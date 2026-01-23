#!/usr/bin/env bash
# Clean orphaned directories from extra_paths globs.
#
# Usage: clean-orphaned-paths.sh <target_dir> <extra_paths...>
#
# For each glob pattern in extra_paths (e.g., plugins/*), removes directories
# in the destination that no longer exist in the source (/tmp/source).

set -euo pipefail

target_dir="$1"
shift

for pattern in "$@"; do
  # Extract the base directory (everything before the first *)
  # Supports patterns like: plugins/*, plugins/*/changelog
  base_dir="${pattern%%\**}"
  base_dir="${base_dir%/}"

  # Skip if pattern has no wildcard (rsync --delete handles it)
  [[ "$pattern" != *"*"* ]] && continue

  # Skip if base_dir is empty (pattern starts with *)
  [[ -z "$base_dir" ]] && continue

  # Safety: verify source exists
  if [[ ! -d "/tmp/source/$base_dir" ]]; then
    echo "Warning: source directory /tmp/source/$base_dir does not exist, skipping cleanup"
    continue
  fi

  dest_base="$target_dir/$base_dir"

  # Safety: verify dest_base is under target_dir
  if [[ "$dest_base" != "$target_dir"/* ]]; then
    echo "Error: dest_base '$dest_base' is not under target directory, skipping"
    continue
  fi

  # Check each subdirectory in destination
  if [[ -d "$dest_base" ]]; then
    for dest_subdir in "$dest_base"/*/; do
      [[ -d "$dest_subdir" ]] || continue
      subdir_name=$(basename "$dest_subdir")

      # If source doesn't have this directory, remove it from destination
      if [[ ! -d "/tmp/source/$base_dir/$subdir_name" ]]; then
        echo "Removing orphaned directory: $dest_base/$subdir_name"
        rm -rf "$dest_subdir"
      fi
    done
  fi
done
