This release fixes an issue that broke file uploads in the Explorer on Tenzir Node v6. It also updates the platform user interface container images to clear vulnerabilities found in the weekly container scan.

## 🐞 Bug fixes

### Container image dependency security fixes

The `platform-ui` and `platform-ui-aws` container images have been updated to resolve vulnerabilities found in the weekly container scan. The changes are transparent at runtime and require no configuration or data migration.

The frontend upgrades the following Node dependencies:

- `fast-uri` 4.1.2 to 4.1.4: CVE-2026-75899, CVE-2026-75931, CVE-2026-76172, CVE-2026-75975
- `postcss` 8.5.26 to 8.5.28, which moves its nested `nanoid` copy from 3.3.17 to 3.3.18: CVE-2026-67213

*By @lava.*

### Fix Explorer file upload on Tenzir Node v6

Dropping a file into the Explorer produced a pipeline that failed with `error: expected record` on Tenzir Node v6. The generated pipeline used `from "<url>"`, and the v6 executor no longer infers a loader and parser from a URL argument.

The Explorer now generates `from_http "<url>" { read_auto }` for nodes that support it, and keeps the old form for nodes older than v6.3.0. The generated pipeline carries a `// neo: true` directive, because `read_auto` requires the new executor that a node can otherwise turn off.

*By @lava.*
