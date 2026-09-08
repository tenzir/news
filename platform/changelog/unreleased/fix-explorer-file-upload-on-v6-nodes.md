---
title: "Fix Explorer file upload on Tenzir Node v6"
type: bugfix
author: lava
created: 2026-09-08T12:30:00Z
---

Dropping a file into the Explorer produced a pipeline that failed with
`error: expected record` on Tenzir Node v6. The generated pipeline used
`from "<url>"`, and the v6 executor no longer infers a loader and parser from a
URL argument.

The Explorer now generates `from_http "<url>" { read_auto }` for nodes that
support it, and keeps the old form for nodes older than v6.3.0. The generated
pipeline carries a `// neo: true` directive, because `read_auto` requires the
new executor that a node can otherwise turn off.
