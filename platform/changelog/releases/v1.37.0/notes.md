Organizations can now maintain their own package libraries by adding public or private Git repositories alongside the built-in Tenzir Library. This release also speeds up data loading in the app and adds a Force stop action for pipelines that are slow to drain.

## 🚀 Features

### Admin command to mint workspace keys

Platform administrators can now mint keys for arbitrary workspaces with the new `tenzir-platform admin create-user-key <workspace_id> <user_id>` command.

*By @lava.*

### Custom library sources

Organizations can now maintain their own package libraries.

From the organization settings page, an administrator can add up to 10 library sources — public or private Git repositories — alongside the built-in Tenzir Library, which is always available and does not count toward the limit. A private source authenticates with a credential you provide; it is stored securely and used only on the server, so it is never exposed to the browser.

The Library then shows packages from every configured source together, labels each package with the source it came from, and lets you filter the view by source.

*By @gitryder.*

### Force stop action for pipelines

The pipeline menu now offers a **Force stop** action that terminates a running, paused, or stopping pipeline immediately instead of waiting for it to drain in-flight data.

Use **Force stop** when a pipeline is taking too long to stop — for instance, when it is stuck in the `stopping` state. The action appears only for nodes that support it.

*By @aljazerzen and @claude.*

## 🔧 Changes

### Improve performance of the app

Data loaders and Explorer queries in the app could sometimes be delayed by multiple seconds, depending on the load on the node, the amount of data being loaded in paralell by the app, and whether the app was running on HTTP/1.

This change brings a new way that the app can load data from the node that isn't subject to these limitations. This is made possible by the release of Tenzir Node version 6.7.0. So if you're experiencing slow data loading in the app, try upgrading your nodes to 6.7.0 first.

*By @avaq.*

### Remove the Random Example feature

The button for filling a random example into the Explorer has been removed. The Explorer now loads the examples lazily when the example panel is opened.

*By @avaq.*
