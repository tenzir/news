This release adapts the Explorer to the new data model in Tenzir Node 6.20. The Explorer now groups events by schema name and shows accurate per-name counts, even when field sets differ.

## 🐞 Bug fixes

### Explorer schema grouping by name

Explorer now shows events with the same schema name together, even when their fields differ. The schema list shows accurate counts by name, and missing fields appear as empty table cells. Events with different names remain separate even when they have the same fields.

Schema-filtered Stream views keep their selection when added to a dashboard, and IP and subnet columns sort by address rather than spelling.

Nodes without the `serve-name-and-type` feature can still run pipelines and view their events in Stream view. Upgrade to Tenzir Node 6.20 or later for schema browsing, tables, and charts.

*By @aljazerzen.*
