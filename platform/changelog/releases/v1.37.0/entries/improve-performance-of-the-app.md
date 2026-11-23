---
title: Improve performance of the app
type: change
author: avaq
created: 2026-07-13T14:16:56.450Z
---

Data loaders and Explorer queries in the app could sometimes be delayed by
multiple seconds, depending on the load on the node, the amount of data being
loaded in paralell by the app, and whether the app was running on HTTP/1.

This change brings a new way that the app can load data from the node that isn't
subject to these limitations. This is made possible by the release of Tenzir
Node version 6.7.0. So if you're experiencing slow data loading in the app, try
upgrading your nodes to 6.7.0 first.
