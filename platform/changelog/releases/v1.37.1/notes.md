The 1.37.0 performance improvements now work more reliably, and this release fixes package loading and login redirects.

## 🐞 Bug fixes

### Fix performance optimization not working for newly created nodes

We fixed an issue where the performance optimization we made in 1.37.0 didn't start working for newly spawned nodes until after a page reload.

*By @avaq.*

### Fix weird redirect after login

Sometimes after your session expired and you were logged out, logging back in would put you on a page with raw data instead of the user interface. This has now been fixed.

*By @avaq.*

### Installed package loading in the Library

The Library now loads installed packages from connected nodes without failing schema validation. This restores installation status, update detection, and package management for nodes with existing packages, including Tenzir v5.x and v6.x nodes.

*By @zedoraps and @codex.*
