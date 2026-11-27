# Manifest

The source of truth is one YAML file per plugin. Every target runtime reads it. Do not keep a second hand-written copy of the actions in TypeScript, Python, or Rust.

Card generation: the actions, args, and results section of the card is built from this file. The loop section lives only in a sibling `card-loop.md` (stored as `loop_text`). That file is the single source the linter reads. There is no `loop:` field in the YAML; an unknown top-level key fails validation.

## Required shape

```yaml
id: code.tests
title: Code tests
version: 1
when: Run the repo tests, wake when they finish, and fix until every test is green.
entrypoint: ./index.mjs
self_test: ./self_test.mjs
actions:
  - name: code.tests.run
    description: Start the test command in this workspace. Returns a job id.
    idempotency_key: "code.tests.run:${workspace_id}:${command}"
    args:
      command:
        type: string
        description: Test command. Omit to use the workspace setting or autodetect.
    result:
      type: object
      additionalProperties: false
      required: [ok, kind]
      properties:
        ok: { type: boolean, description: "True whenever the plugin ran, including work_failed; false only on plugin_error." }
        kind:
          type: string
          enum: [ok, work_failed, plugin_error]
          description: ok if accepted and running or passed; work_failed only on finished failing results; plugin_error if it could not start.
        job_id: { type: string, description: Host job id. Present unless plugin_error. }
        retry_key: { type: string, description: Idempotency key for the wake. }
        artifact: { type: string, description: Path to the test-results table when written. }
permissions:
  secrets: []
  paths: ["/workspace", "/work/.plugins"]
  network: on
budget:
  timeout_s: 1200
  stall_s: 180
  progress_s: 15
  result_chars: 4000
wake:
  events: [job.finished]
  retry_key: "code.tests:${job_id}"
state:
  location: /work/.plugins/code.tests
retry:
  on: [plugin_error]
  max: 1
```

See [code-plugin-example.md](code-plugin-example.md) for the complete worked example.

## Field reference

Top-level keys:

| Field | Required | Default | What it is |
|---|---|---|---|
| `id` | yes | | Plugin id, dotted, stable. Usually `namespace.noun`. |
| `title` | yes | | Short human name, sentence case. |
| `version` | yes | | Positive integer. Incremented on each promoted draft. Do not skip versions by hand. |
| `when` | yes | | One sentence for the discovery index. |
| `entrypoint` | yes | | Module the wrapper loads. One exported function per action; no branching on plugin id. |
| `self_test` | yes | | Command or module the promote gate runs. Must cover `ok`, `work_failed`, and `plugin_error`. |
| `actions` | yes | | List of actions. At least one. |
| `permissions` | no | see below | Secrets by name, path scope, network. |
| `budget` | no | see [options](options.md) | Time, stall, progress, result cap. |
| `wake` | no | no wake | Events that may start or continue a turn. |
| `state` | no | none | Where the plugin keeps work in progress. |
| `retry` | no | no automatic retry | When the wrapper may retry a `plugin_error`. Never retry a successful `work_failed`. |

Each action:

| Field | Required | Default | What it is |
|---|---|---|---|
| `name` | yes | | `namespace.noun.verb`, lowercase snake_case dotted segments (2 to 4 segments). |
| `description` | yes | | At most 160 characters. |
| `args` | no | no args | Map of name to a JSON Schema object. Every arg has `type` and `description`. Objects set `additionalProperties: false`. |
| `result` | no | plugin-level result, or `{ok, kind}` | JSON Schema for the canonical result. |
| `timeout_s` | no | `budget.timeout_s` | Per-action cap. |
| `dry_run` | no | `false` | If true, the action can plan without writing. |
| `confirm` | no | `false` | Needs a person's yes on surfaces that ask. |
| `read_only` | no | `false` | Changes nothing. May run in parallel with other read-only actions. |
| `idempotency_key` | yes on mutating actions, omitted on `read_only` | | Template so a retry cannot double-run. Required on `run` and `cancel`. |

`permissions`:

| Field | Required | Default | What it is |
|---|---|---|---|
| `secrets` | no | `[]` | Names of secrets the plugin may request. Values never go in the manifest, card, or result. |
| `paths` | no | omitted (the agent's existing access) | Paths that narrow write scope. Omitting does not shrink access, and the parser must not insert a default list. |
| `network` | no | `on` | Network is on by default. Set `off` to opt out. |

`wake`:

| Field | Required | Default | What it is |
|---|---|---|---|
| `events` | yes if `wake` is set | | Event names (e.g. `job.finished`) emitted by the host. |
| `retry_key` | yes if `wake` is set | | Template used as the idempotency key on the wake webhook. A second post with the same key is ignored. |

`state.location` is a path or a store key inside the workspace or plugin store. Never point it at a secret path.

Unknown top-level keys fail validation. They do not warn.

## Lint

The validator fails when:

- A required field is missing, or a field has the wrong type.
- An action name fails `namespace.noun[.verb]` syntax, or a description is empty or longer than 160 characters.
- The card loop (`card-loop.md`) names an action that is not in the manifest.
- The card loop has no line starting with `Done when:`.
- The loop is longer than about one screen (40 lines hard cap).
- `network` is anything other than `on` or `off`.
- `secrets` contains a value that looks like a token (`ghs_`, `sk-`, etc.). Names only.
- Two actions share a name, or two plugins in the same index share an id.
- `entrypoint` or `self_test` is missing, or `self_test` escapes the plugin folder (absolute path or `..`).
- A mutating action (`read_only` not true) lacks `idempotency_key`, or a `read_only` action declares one.

Fix the file. Do not add a lint-ignore comment.
