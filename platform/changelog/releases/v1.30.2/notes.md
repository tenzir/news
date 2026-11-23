This release fixes an issue where the pipeline table stayed filtered after navigating away from a pipeline's detail page. It adds thousands separators to numeric values in the Insights tab for better readability. It also updates dependencies to address security issues.

## 🔧 Changes

### Readable numbers in the Insights tab

We added thousands separators to numeric values in the pipeline Insights tab, making large numbers easier to read at a glance.

*By @gitryder.*

## 🐞 Bug fixes

### Fix pipeline table filter not clearing

We fixed an issue where the pipeline table stayed filtered after viewing a pipeline's detail page and navigating away to another tab. Returning to the Pipelines page would show only the previously viewed pipeline, and clearing the search had no effect.

*By @gitryder.*
