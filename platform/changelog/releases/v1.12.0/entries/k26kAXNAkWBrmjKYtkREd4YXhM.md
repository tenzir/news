---
title: "Improvements to the Ingress/Egress data visualization"
type: change
author: avaq
created: 2025-12-17T13:24:10Z
---

- The daily throughput widget now shows the number of bytes for the window that exactly matches the 24h range from the last seen data point, including smooth interpolation.
- The ingress/egress data shown now gets more realtime updates.
- The ingress/egress graph's X domain was made more stable, meaning there's no sudden jumps in the graph's X axis when new data is shown.
