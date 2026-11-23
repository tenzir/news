This release unifies the library's Available and Installed tabs into a single view, making package management more streamlined. It also adds pipeline activity sorting, series isolation in activity charts, a line wrap toggle in the Inspector, platform version display, and a backslash escaping fix.

## 🚀 Features

### Isolate series in pipeline activity chart

You can now click on the Ingress or Egress legend item to isolate that series in the activity chart. Clicking again shows both series, making it easier to analyze each metric when lines overlap.

*By @gitryder in #64.*

### Sort pipelines by activity

We added sorting for the Live Activity column in the pipelines table, so you can easily order pipelines by their activity level.

*By @gitryder in #38.*

### View the current platform version

We now display the current platform version at the bottom of the workspace switcher dropdown,️ making it easier to always see which version you’re on.

*By @gitryder in #42.*

### Wrap lines in the Inspector

We added a toggle in the Explorer table Inspector that lets you wrap lines for easier reading.

*By @gitryder.*

## 🔧 Changes

### Unified library tabs

We unified the Available and Installed library tabs into a single view, so you can see which packages are installed without switching tabs. You can also uninstall packages directly from the same page.

*By @gitryder in #29.*

## 🐞 Bug fixes

### Fixed backslash escaping in TQL string rendering

We fixed a bug in the Inspector where strings containing backslashes were not displayed correctly. Backslashes were not being escaped in TQL string rendering. For example, a string like `Hello \World\` was previously rendered as `"Hello \World\"` instead of `"Hello \\World\\"`. The fix ensures backslashes are properly escaped when displayed.

*By @lava.*
