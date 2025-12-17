---
title: "Fix 'View'-button in failed pipeline Toast"
type: bugfix
author: avaq
created: 2025-12-17T13:24:10Z
---

When a deployed pipeline fails, a "Toast" popup is shown in the bottom right that allows you to view the error, except, that button didn't work. Now it does!

And while we were at it, we also improved the text for these toasts a little to make it clearer that it's specifically about a *deployed* pipeline.
