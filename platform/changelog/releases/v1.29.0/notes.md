With this release, the Tenzir Platform preserves deep links through the login flow, so users are redirected to their original destination after signing in. It also includes several bug fixes and a performance improvement for loading across the platform.

## 🚀 Features

### Preserve deep links through login flow

When you click a deep link in Tenzir Platform but aren't logged in, you're now redirected to your original destination after signing in, instead of landing on the home page.

*By @lava.*

## 🔧 Changes

### Faster loading across the platform

We improved how the nodes list loads, making dependent views feel faster and more responsive across the platform.

*By @gitryder.*

## 🐞 Bug fixes

### Fix blocked profile images for some login providers

We fixed an issue where profile images from Gravatar and Microsoft accounts were blocked by the content security policy, causing broken or missing avatars.

*By @gitryder.*

### Fix diagnostics showing data from the wrong pipeline

We fixed an issue where the diagnostics pane could show diagnostics from a different pipeline than the one currently open in the detail modal.

*By @gitryder.*

### Fix unintended logout on inaccessible workspace links

We fixed an issue where opening a pipeline link for a workspace you don’t have access to would log you out. You are now redirected to the access page where you can open the link in your default workspace.

*By @gitryder.*

### Fix unstable context list order

We fixed an issue where the context list could appear in a random order when no search was active, causing items to jump around. The list now uses a stable alphabetical order so it stays consistent and easier to interact with.

*By @gitryder.*
