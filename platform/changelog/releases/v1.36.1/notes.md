This release fixes a performance issue in the websocket gateway. Previously, heavy secret request traffic could slow down all gateway responses by several seconds.

## 🐞 Bug fixes

### Slow gateway responses under secret request load

The websocket gateway is now significantly faster in deployments with many secret requests. Previously, heavy secret request traffic could slow down all gateway responses by several seconds.

*By @lava.*
