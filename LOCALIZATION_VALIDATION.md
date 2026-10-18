# Localization validation

Validation is limited to static checks. No project code was executed, no dependencies were installed, and no accounts or platform connections were configured.

## Passed

- Parsed and compiled all 71 Python files without executing them.
- Compared all 26 modified runtime Python files against the upstream commit: program structure and non-string values are unchanged after excluding localized string content and literal f-string display fragments.
- Checked all 3 shell scripts with `bash -n` (syntax only).
- Checked changes with `git diff --check`.
- Parsed SVG XML, project TOML, and JSON configuration.
- Checked relative Markdown and HTML links.
- Confirmed both packaged skill variants contain the same English instructions.
- Confirmed the license, package/dependency definitions, dependency constraints, example environment file, and mcporter configuration are byte-for-byte unchanged.
- Reviewed retained non-English strings and updated assertions tied to translated output. Multilingual inputs and security-policy markers remain in the tests.

## Not run

- The pytest unit/integration suite
- Runtime CLI commands or health checks
- Dependency installation or package/wheel builds
- Live platform/API/browser integration tests
- Ruff and mypy (not available in this workspace)

Static checks do not prove runtime or live-platform compatibility. This edition changes language, not integration capabilities. Review the source before installation and run the normal upstream development checks in an approved environment if runtime verification is required.

## Retained compatibility identifiers

These original backend names are preserved because they may be used in saved routing configuration or program output:

- `B站搜索 API`: Bilibili search API
- `Xueqiu API (需要登录 Cookie)`: Xueqiu API (login cookies required)
- `内置`: built-in

The CLI also recognizes the upstream login response `已登录` (“logged in”). Other intentionally retained strings are documented in [ENGLISH_EDITION.md](ENGLISH_EDITION.md).
