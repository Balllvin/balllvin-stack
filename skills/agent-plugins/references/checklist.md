# Checklist

Run this before you promote a draft or open a PR that adds a plugin.

- [ ] The job and the done-condition are each one sentence. They match.
- [ ] No second done-condition is hiding in the loop. If there is one, split the plugin.
- [ ] The card loop fits on about one screen and has a `Done when:` line.
- [ ] The loop names only actions in the manifest. Lint fails, not warns.
- [ ] Action names match `namespace.noun.verb` and descriptions are at most 160 characters.
- [ ] Results set `kind` to `ok`, `work_failed`, or `plugin_error`. `ok` is true whenever the plugin ran, including `work_failed`, and false only on `plugin_error`. Typed failures are `file:line:reason` plus an artifact path. No raw logs.
- [ ] Mutating actions have an `idempotency_key`. Wakes have a `retry_key`.
- [ ] Context injection (`inject()`) is not used as a wake. The wake is the host webhook (with optional in-session followup shortcut).
- [ ] `permissions.network` is `on` unless this plugin must not use the network (`off` on purpose).
- [ ] Secrets are named, never valued. Paths are scoped. Sensitive/money plugins are locked and never reachable from analysis plugins.
- [ ] Dry-run or `validate`, `cancel`, progress pings, and a stall timeout are present when the plugin can start a job.
- [ ] The self-test covers a happy path, a `work_failed` path, and a break. It fails when the plugin is broken.
- [ ] A held-out eval exists, with three baseline runs. The log names the pinned plugin version and harness version.
- [ ] The draft bumps the version. Schema validation and the self-test passed. The reason and author are logged.
- [ ] One manifest source of truth feeds all target runtimes without hand-edited generated catalogs.
