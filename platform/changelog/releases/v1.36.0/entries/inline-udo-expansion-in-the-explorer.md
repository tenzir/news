---
title: Inline UDO expansion in the Explorer
type: feature
authors:
  - Zedoraps
  - claude
created: 2026-06-16T20:19:22.81251Z
---

User-Defined Operators (UDOs) referenced in a pipeline can now be expanded
inline to see their body without leaving the editor.

In the Explorer and in the Pipelines detail modal, every UDO call is marked
with a dotted underline and a chevron in the gutter. Click either the
operator name or the chevron to open a read-only block widget directly
below it. The body is rendered with full TQL syntax highlighting — the same
look as the main editor — pulled live from the connected node's package
registry.

Use the new toolbar button to expand or collapse every UDO at once,
including all of their nested UDO calls.
Each nested expansion sits one indent deeper with a stronger left-rail
color, so a chain like `fortinet::fortigate::ocsf::map` →
`fortinet::fortigate::ocsf::logs::dlp` →
`fortinet::fortigate::ocsf::network_evidence` stays readable.

In the Pipelines modal, the expansion header notes that the displayed
definition is the current node-registry version and may differ from what
a long-running pipeline is actually executing — Tenzir resolves UDO
references at pipeline-launch time, so a running pipeline keeps its
inlined definition until it is restarted.
