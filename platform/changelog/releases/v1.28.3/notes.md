This release improves the clarity and usability of Explorer charts with better legends, tooltips, and an expanded color palette. It also fixes several UI bugs including unresponsive pipeline lists and stale workspace cleanup.

## 🔧 Changes

### Improved Chart Legends, Tooltips, and Colors

We improved the clarity and usability of Explorer charts. Legends are now collapsible, easier to read, and support filtering series directly. Pie chart legends adapt better to available space, and tooltips provide clearer information.

We also expanded the chart color palette for better visual distinction between series, fixed bar chart x-axis labels overlapping when there are many data points, and refined chart layout and behavior for a smoother overall experience.

*By @gitryder.*

## 🐞 Bug fixes

### Fix pipeline list not responding after pressing ESC

We fixed an issue where pressing ESC to close a pipeline detail view caused the pipeline list to stop responding to clicks.

*By @gitryder.*

### Fix stale loop variables in static workspace cleanup

Fixed a bug where the static workspace synchronization used stale loop variables during cleanup, causing stale workspaces to persist and the last configured workspace to be incorrectly deleted.

*By @lava.*

### Fix workspace switcher not displaying Google profile pictures

Resolved an issue where your Google profile picture did not appear in the workspace switcher. The image now loads and displays correctly.

*By @gitryder.*
