---
title: Field actions and cached value insights in the Explorer
type: feature
authors:
  - zedoraps
created: 2026-08-02T22:20:48.584928Z
---

You can now right-click fields and values in collapsed or expanded Explorer Stream events, as well as in the Table and Inspector views, to build filters and field operations without writing them manually. Available actions depend on the field and value, including equality and comparison filters, string matching, timestamp windows, field selection, and field removal. You can also hide or show a non-timestamp field in the collapsed Stream overview and the Table view.

Hover over **Top values**, **Rare values**, or **Count values** to preview value frequencies from the current Explorer cache without replacing your pipeline. The preview respects the active result schema or Stream schema filters and becomes available once the run has finished; while a run still streams, the menu offers actions that add the equivalent step to your pipeline instead. Select **Open as query** to continue the analysis as a standalone query.
