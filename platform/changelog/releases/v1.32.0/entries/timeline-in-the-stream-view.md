---
title: Timeline in the Stream view
type: feature
authors: gitryder
created: 2026-05-06T08:04:39.151334Z
---

The Stream view now includes a timeline that shows event volume over time,
segmented by schema. It automatically detects timestamp fields and adapts 
its bucket size to the data’s time range, providing an at-a-glance view of
when events occur and which schemas are most active.

It also probes your data for time fields and shows availability inline, 
omitting events without a recognized time field (ts, timestamp, or time).
