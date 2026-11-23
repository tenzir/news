This release fixes a bug where users could experience authentication failures due to stale user keys in their session. The platform now proactively checks for expired keys and refreshes them automatically.

## 🐞 Bug fixes

### Fixed workspace switcher on pipeline detail page

We fixed an issue where the workspace switcher dropdown did not open on the pipeline detail page.

*By @gitryder in #56.*

### User key expiration handling

Fixed a bug that could leave users with a stale user key in their session, causing authentication failures. The platform now proactively checks for expired user keys and refreshes them automatically.

*By @lava.*
