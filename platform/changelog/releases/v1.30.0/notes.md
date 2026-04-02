This release introduces a new Stream view in the Explorer that displays pipeline results as a continuous, expandable event list. It also adds a time range selector, sortable table columns, and copyable inspector values, alongside several bug fixes for package management and the library view.

## 🚀 Features

### Copyable field names and values in the inspector

You can now click on field names and values in the Explorer inspector to copy them to the clipboard. Field names copy the full dot-separated path, and values copy their TQL representation.

*By @gitryder.*

### Sortable columns in the Explorer table

You can now sort the Explorer table by clicking column headers. Sortable columns show a sort indicator, and clicking cycles through ascending, descending, and unsorted states. Sorting works for both top-level and nested fields.

*By @gitryder.*

### Stream view in the Explorer

We added a new Stream view to the Explorer that shows all pipeline results as a continuous list of expandable events. You can switch between the Table, Chart, and Stream views using the view selector in the toolbar. The Stream view displays events from all schemas together, with color-coded badges to distinguish between them. Each row shows a one-line preview that you can expand to inspect the full event. The view remembers your selection across pipeline runs, and the event list scrolls horizontally as a whole, with schema badges staying pinned on the left.

*By @gitryder.*

### Time range selector in the Explorer

You can now select a time range directly from the Explorer header. Choose from quick presets like 5 minutes or 12 hours, or open the custom popover to pick from a grid of relative durations or set an absolute date range. The selector is currently available for pipelines that start with the `export` operator.

*By @gitryder.*

## 🔧 Changes

### Unified package detail view in the library

We combined the 'About' and 'Install' tabs in the package detail drawer into a single scrollable view. Package information, examples, and configuration options are now shown on one page instead of requiring tab switches.

*By @gitryder.*

## 🐞 Bug fixes

### Fix rotated text in package detail accordion

We fixed a bug where operator description text on the package detail page appeared rotated 90 degrees, overlapping other content.

*By @gitryder.*

### Package installs for packages with user-defined operators

Packages containing user-defined operators can again be installed through the platform. Previously, installing such packages failed because the operator arguments were serialized incorrectly. This only affected installs through the platform UI—command-line package installs were not impacted.

*By @gitryder.*

### Show custom packages in the library view

We fixed an issue where custom packages installed on a node were not visible in the library view. Previously, only packages from the official Tenzir library were shown. Custom packages are now included alongside library packages.

*By @gitryder.*
