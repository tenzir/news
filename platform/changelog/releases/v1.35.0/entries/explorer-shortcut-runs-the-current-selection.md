---
title: Explorer shortcut runs the current selection
type: bugfix
authors:
  - Zedoraps
  - codex
created: 2026-06-22T12:07:47.767548Z
---

The Explorer now runs the current editor selection when using the keyboard shortcut.

Previously, selecting text with `Ctrl+A` and then pressing `Ctrl+Enter` while still holding `Ctrl` could run an older selection instead of the newly selected pipeline.
