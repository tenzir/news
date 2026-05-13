This is a security patch release that updates dependencies to address vulnerabilities. It also shortens the default user key expiry to 15 Minutes.

## 🔧 Changes

### Shorten default user key lifetime

We reduced the default lifetime of user keys from one week to 15 minutes. Sessions transparently refresh, so this is invisible in normal use, but shortens the window in which a leaked key could be reused.

*By @lava.*
