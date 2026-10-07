---
title: Detailed reason for invalid JSON errors in the Explorer
type: change
authors:
  - tobim
created: 2026-10-07T07:05:26.966129Z
---

When the Explorer fails to read a pipeline result because a node response is not valid JSON, the error details now include the exact reason, such as a duplicate key and its position:

```
Decode: invalid JSON: Duplicate key 'url' encountered at position 4711
```

Previously, the error only said `invalid JSON`, which made it hard to tell what was wrong with responses that other tools accept.
