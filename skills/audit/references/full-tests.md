# Full tests

Load when the mode is Full tests, or when the ask is to run all tests or fix all failing tests across the whole repository.

This mode runs tests only (unit, integration, and repository contract suites). It does not add production builds, linters, or e2e browser suites unless requested.

## Order and isolation

Run suites app by app in dependency order (**backend / core data layer first**, then compiled/worker harnesses, then web/client apps, then contract and migration suites). Stream stdout and stderr to a dedicated run log outside the repo (e.g. `/tmp/full-tests-<timestamp>.log`).

- Derive exact file lists, environment variables, and throwaway database setup from your repository's CI job definitions (`scripts/ci/` or `.github/workflows/`) rather than inventing ad-hoc commands.
- Use throwaway local test databases and isolated working directories; drop scratch databases when finished.
- Never score passes against a stale failure baseline or relax timeouts/assertions to go green.

## Repair loop

1. Start suites in order, triaging failures as they appear without waiting for the last app.
2. When a test fails, decide whether the test is wrong (contract changed) or the code is wrong, and fix only that root cause. Never skip, xfail, or loosen a test.
3. After each fix lands on its branch, re-run that app's full suite.
4. Before finalizing, merge all fixes into a clean verification worktree and re-run every suite from scratch to confirm zero cross-app regressions.
