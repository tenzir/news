This release upgrades frontend, backend, and CLI dependencies, along with the tenzir-seaweed base image, to address known vulnerabilities reported by our container scanner. It also fixes two chart issues: tooltips no longer get clipped in small dashboard cells, and charts no longer zoom unexpectedly on click.

## 🐞 Bug fixes

### Fix accidental chart zoom on click

We fixed an issue where clicking on a line, area, or bar chart could unintentionally zoom the chart to a narrow window, hiding the axis labels and most of the data. Charts no longer respond to clicks this way.

*By @gitryder.*

### Fix chart tooltip clipping

We fixed an issue where chart tooltips were cut off in dashboard cells and the Explorer chart view when the tooltip did not fit inside the chart area. Tooltips now stay fully visible, even on small cells or near the screen edge.

*By @gitryder.*
