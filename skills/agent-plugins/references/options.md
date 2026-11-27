# Options catalog

Every manifest field, its default, and when to change it. Pair with [manifest](manifest.md).

| Field | Default | Change it when |
|---|---|---|
| `id` | (required) | Never rename a published id. Add a new plugin and deprecate the old one. |
| `title` | (required) | The name a person sees in an index. Change freely; the id stays. |
| `version` | (required, start at `1`) | Bumped on each promoted draft. |
| `when` | (required) | The discovery line is wrong or overlaps a sibling. |
| `entrypoint` | (required) | Module the wrapper loads. One exported function per action, no branching on plugin id. |
| `self_test` | (required) | Command the promote gate runs. Must cover `ok`, `work_failed`, and `plugin_error`. |
| `actions[].name` | (required) | Renaming is public. Add a deprecation/redirect if callers already use the old name. |
| `actions[].description` | (required, max 160) | The model picks the wrong sibling, or text names internal flags. |
| `actions[].args` | none | Action needs input the host does not already have. Omit args the runtime supplies (workspace id, revision stamp). |
| `actions[].result` | `{ok, kind}` | Next action needs an id, path, or count. Keep small. |
| `actions[].timeout_s` | `budget.timeout_s` | One action is a long job (e.g. full test run) and others are short. |
| `actions[].dry_run` | `false` | Action writes and should offer a plan-only path. |
| `actions[].confirm` | `false` | Action is destructive or user-facing (`open PR`, delete). Worker-facing actions cannot use interactive confirm. |
| `actions[].read_only` | `false` | Action changes nothing, allowing parallel calls. |
| `permissions.secrets` | `[]` | Plugin must read a named host-injected secret (name only, never a value). |
| `permissions.paths` | omitted (existing access) | Narrow write scope inside the workspace. |
| `permissions.network` | `on` | Set `off` for pure local checks that need no network. |
| `budget.timeout_s` | `60` | Raise for long jobs (tests use `1200`); lower to catch runaways sooner. |
| `budget.stall_s` | `180` | Progress pings are expected more or less often than 3 minutes. |
| `budget.progress_s` | `15` | Long job should ping more often, or short job is noisy. |
| `budget.result_chars` | `4000` | Inline output size cap. Prefer writing a file artifact and returning its path over raising this. |
| `wake.events` | no wake | Job can outlive the turn; add `job.finished`. |
| `wake.retry_key` | required with `wake` | Include `job_id` so two jobs cannot share a key. |
| `actions[].idempotency_key` | omitted on `read_only`, required on mutating | Action writes or starts a job; include stable parameters so retries cannot double-run. |
| `state.location` | none | Plugin keeps files or state between actions. |
| `retry.on` | no retry | Only `plugin_error`, and only when safe. Never retry `work_failed`. |
| `retry.max` | `0` | One retry is the usual max. More hides real breaks. |

Per-plugin `permissions` are extra scopes the wrapper enforces on top of the sandbox; do not invent undeclared manifest keys without updating the schema and validator first.
