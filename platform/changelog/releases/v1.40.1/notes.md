This release restores scrolling through all schemas in the Explorer's Results tab when the list exceeds the pane height. Errors about invalid JSON responses from a node now also name the exact reason, such as a duplicate key and its position.

## 🔧 Changes

### Detailed reason for invalid JSON errors in the Explorer

When the Explorer fails to read a pipeline result because a node response is not valid JSON, the error details now include the exact reason, such as a duplicate key and its position:

```
Decode: invalid JSON: Duplicate key 'url' encountered at position 4711
```

Previously, the error only said `invalid JSON`, which made it hard to tell what was wrong with responses that other tools accept.

*By @tobim.*

## 🐞 Bug fixes

### Scrolling through Explorer result schemas

You can scroll through all schemas in the Explorer's Results tab again when the list exceeds the pane height. The stored data browser previously made schemas below the visible area unreachable.

*By @zedoraps.*
