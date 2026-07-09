This release introduces inline expansion of User-Defined Operators in the Explorer. Every UDO call in a pipeline can now be expanded in place to reveal its body with full TQL syntax highlighting, including nested UDO calls. It also fixes sporadic 502 errors that could occur when running the platform behind a load balancer.

## 🚀 Features

### Inline UDO expansion in the Explorer

User-Defined Operators (UDOs) referenced in a pipeline can now be expanded inline to see their body without leaving the editor.

In the Explorer and in the Pipelines detail modal, every UDO call is marked with a dotted underline and a chevron in the gutter. Click either the operator name or the chevron to open a read-only block widget directly below it. The body is rendered with full TQL syntax highlighting — the same look as the main editor — pulled live from the connected node's package registry.

Use the new toolbar button to expand or collapse every UDO at once, including all of their nested UDO calls. Each nested expansion sits one indent deeper with a stronger left-rail color, so a chain like `fortinet::fortigate::ocsf::map` → `fortinet::fortigate::ocsf::logs::dlp` → `fortinet::fortigate::ocsf::network_evidence` stays readable.

In the Pipelines modal, the expansion header notes that the displayed definition is the current node-registry version and may differ from what a long-running pipeline is actually executing — Tenzir resolves UDO references at pipeline-launch time, so a running pipeline keeps its inlined definition until it is restarted.

*By @Zedoraps and @claude.*

## 🐞 Bug fixes

### Sporadic 502 errors behind load balancers

The platform's HTTP servers now keep idle connections open longer than typical load balancer idle timeouts. Previously, a load balancer could reuse a pooled connection that the platform had already closed, causing requests to sporadically fail with 502 errors.

In addition, when the list of connected nodes cannot be retrieved, the API now returns the actual error reported by the websocket gateway instead of a generic parsing failure, and requests that were aborted by the client no longer produce error-level noise in the app server logs.

*By @lava.*
