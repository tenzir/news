This release upgrades dependencies to address known security vulnerabilities and fixes an issue where the Insights tab selection could get stuck in an invalid state.

## 🐞 Bug fixes

### Fix Insights tab guard not resetting tab selection

We fixed an issue where switching away from a pipeline that has the Insights tab available to one that does not could leave the tab selection in an invalid state.

*By @realllydan.*

### Upgrade dependencies to fix known vulnerabilities

We upgraded Python dependencies and added system-level package upgrades to the Docker images to address known vulnerabilities.

*By @lava.*
