---
title: 'Fix actions on the account, org, and invite pages failing after the page was open for 15 minutes'
type: bugfix
author: avaq
created: 2026-05-21T11:40:00.000000Z
---

We fixed an issue where actions on the account, organization, and invitation pages would fail if the page had been open for more than 15 minutes. The following operations now automatically refresh the user key when needed: changing account details, updating passwords, deleting accounts, creating and updating organizations, managing organization invitations, and deleting organizations.
