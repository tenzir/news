---
title: "Lower wait times when data loading fails"
type: change
author: avaq
created: 2025-12-17T13:24:10Z
---

When there's an error that prevents the app from being able to load data, the app would previously keep trying for 30 seconds while showing a loading spinner. This has been reduced to 5 seconds so that in case of a problem, the UI will display the error sooner.
