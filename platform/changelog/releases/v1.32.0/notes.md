This release adds a timeline to the Stream view that visualizes event volume over time, segmented by schema, with automatic timestamp detection. The Explorer's table view also gains keyboard navigation between entries and a streamlined Fields popover for quicker field selection.

## 🚀 Features

### Keyboard navigation between entries in Explorer

You can now navigate between entries in the Explorer table using arrow keys. Press Space to toggle the inspector, then use Arrow Up and Arrow Down to move between rows and seamlessly across pages.

*By @gitryder.*

### Timeline in the Stream view

The Stream view now includes a timeline that shows event volume over time, segmented by schema. It automatically detects timestamp fields and adapts its bucket size to the data’s time range, providing an at-a-glance view of when events occur and which schemas are most active.

It also probes your data for time fields and shows availability inline, omitting events without a recognized time field (ts, timestamp, or time).

*By @gitryder.*

## 🔧 Changes

### Improved field selection in the table view

We moved field selection in the Explorer's table view into a dedicated popover. The 'Fields' button sits in the toolbar and shows how many fields are currently hidden. Opening it reveals the full field list with the same click-to-toggle and shift+click-to-focus behavior as before.

*By @gitryder.*

### Insights tab now available for every pipeline

The Insights tab in the pipeline detail view is no longer experimental and now appears for every pipeline. It shows you live per-operator CPU usage, events per second, batch ratios, and queue backpressure for the selected pipeline. You can see at a glance which operators are working hardest and where data is piling up, so finding hotspots and tuning pipeline performance becomes easier. Update your node to v6 to see the data.

*By @gitryder.*
