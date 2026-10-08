---
title: Explorer schema grouping by name
type: bugfix
authors:
  - aljazerzen
created: 2026-10-08T15:49:27.874154Z
---

Explorer now shows events with the same schema name together, even when their fields differ. The schema list shows accurate counts by name, and missing fields appear as empty table cells. Events with different names remain separate even when they have the same fields.

Schema-filtered Stream views keep their selection when added to a dashboard, and IP and subnet columns sort by address rather than spelling.

Nodes without the `serve-name-and-type` feature can still run pipelines and view their events in Stream view. Upgrade to Tenzir Node 6.19 or later for schema browsing, tables, and charts.
