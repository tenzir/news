This release fixes an issue that prevented users from enrolling in two-factor authentication with certain authentication provider configurations, most notably on app.tenzir.com. It also stops the diagnostics heatmap from flashing every ten seconds when the selected time window contains many diagnostics.

## 🐞 Bug fixes

### Fix 2FA enrollment

We fixed an issue where user enrollement for 2-factor authentication wasn't working with some authentication provider configurations (most notably on app.tenzir.com).

*By @avaq and @lava.*

### Fix diagnostics-heatmap flashing

We fixed in issue where if there were a lot of diagnostics in the selected diagnostics-heatmap time window, the heatmap would flash every 10 seconds.

*By @avaq.*
