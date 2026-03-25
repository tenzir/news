---
title: Organization and workspace collaboration API
type: feature
author: lava
created: 2026-03-25T13:46:12.554211Z
---

Organizations provide collaborative workspaces for teams on the Tenzir platform. The new organizations API allows users to create organizations, manage memberships, and control workspace access through invitations.

## Core Features

**Organization Management**: Create organizations with `tenzir-platform org create <name>` and delete them with `tenzir-platform org delete`. View organization details and members using `tenzir-platform org info`.

**Membership Control**: Add users to organizations through invitation links. Admins can create invitations with `tenzir-platform org invite [--role=<role>] [--label=<label>]`, where role defaults to "member" but can be set to "admin". Users redeem invitations with `tenzir-platform org redeem-invitation <token>`. Admins revoke pending invitations with `tenzir-platform org revoke-invitation <invitation_id>` and remove members with `tenzir-platform org remove-member <user_id>`.

**Workspace Ownership**: Organizations own workspaces, enabling shared infrastructure management. Create organization-owned workspaces with `tenzir-platform workspace create --name=<name>` (when in an organization context). List and manage organization workspaces with `tenzir-platform workspace list-invitations` and `tenzir-platform workspace revoke-invitation <invitation_id>`.
