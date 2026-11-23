---
title: "Pipeline page widgets"
type: feature
authors: [gitryder, avaq, dit7ya]
created: 2025-12-17T13:24:10Z
---

**Introduction**

The pipeline page now features four widgets placed above the table of pipelines. These widgets provide information about pipelines shown below, as well as allow you to further filter down the list of pipelines.

**The Status Widget**

The first widget, placed in the top left of the screen, shows the total number of pipelines found after search and filtering. It also shows a breakdown of how many pipelines exist for each of 4 statuses:

- `Running`,
- `Completed`,
- `Failed` or
- `Stopped`.

Clicking on one of these status buttons will filter to pipelines with that particular status. Holding the <kbd>Shift</kbd> key while clicking will add the selected status to your current filter instead of replacing it.

The status widget replaces the pipeline state filtering feature found in the pipelines table header, which has now been removed.

**The Daily Ingress/Egress Widget**

Just below the Status Widget is a widget that shows the total ingress and egress traffic for all pipelines after search and filtering, and the percentage difference between the two.

**The Ingress/Egress Chart Widget**

To the right of the other two widgets, the Ingress/Egress Chart shows a graph of all combined ingress and egress for the pipelines after searching and filtering. It supports a few different periods which can be selected from a drop-down.

**The Diagnostics Widget**

On the rightmost side of the widgets row you'll find a heatmap visualizing how many pipelines experienced warnings or errors, with four-hour cells. Searching or otherwise filtering the list of pipelines will update this widget to reflect the new set of pipelines.

Clicking on a cell will filter the list of pipelines to contain only those pipelines that encountered warnings or errors during the corresponding time period. Clicking again will remove the filter.

The time range selected for the diagnostics is also used for the diagnostics column in the pipeline list below.
