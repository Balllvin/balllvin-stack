# Wording

Keep tool descriptions, results, and error contracts crisp so the model does not guess or loop.

## Names

Action names use lowercase snake_case dotted segments: `namespace.noun[.verb]`, two to four segments. The plugin id is the namespace plus the noun (`code.tests`, `equity.valuation`). Actions add the verb (`code.tests.run`, `code.tests.cancel`).

Name the job the model is doing, not the mechanism. `code.tests.run` is right; `vm.exec_pytest` is not.

Use consistent verbs across siblings: `list`, `get` or `read`, `run`, `cancel`, `status`, `validate`. Do not invent a fourth spelling of an existing verb.

## Descriptions

Each action description is at most **160 characters**, verb first, one or two sentences: what it does, then when to use it or how it differs from a sibling. The plugin `when` line is separate and even shorter: one sentence for the discovery index, no action names required.

Do not paste the loop into the description. The loop lives in the card. Do not name internal flags or runtime implementation ids.

## Results the model can use

Return the smallest structured value that lets the model take the next step. Writes return a short status plus the ids needed to chain. Do not echo a body the model just sent. Do not return raw logs.

## Typed failures

A failure the model should act on is one line:

```text
path:line:reason
```

plus a path to a small artifact when the reason needs more than one line (the failing assertion, a truncated stack). Example:

```text
tests/test_plugin_store.py:41:expected promoted version 2, got 1
artifact: /work/artifacts/<turn>/test-results.json
```

Never dump a raw log into the result. If the log matters, write it to an artifact and point at it.

## Two failure kinds

Say which kind it is, every time:

- `plugin_error`: the plugin broke (bad manifest, a self-test failure, a wrapper timeout, a missing permission the manifest required). The model should not retry the same action to "fix the work." Tell it to report the break or call `validate`.
- `work_failed`: the plugin ran, and the job is not done (tests failed, a filing was missing, a validation input check did not pass). The model should follow the loop: edit the failing files with ordinary file tools, then rerun. A running job is never `work_failed`.

A `work_failed` result is a successful plugin execution with a non-green outcome (`ok: true, kind: "work_failed"`). Do not throw it as `plugin_error`.

## Caps

Results are capped. A cap must say three things in plain text: what is shown, the total, and the exact next call (or artifact path) that gets the rest. Silent truncation is a plugin bug. Default caps and how to raise them are in [options](options.md).

## Dry-run, validate, cancel, progress, stall

Every plugin that can start a long-running or mutating job exposes:

- `validate` (or `dry_run` on mutating actions): plan only, no writes.
- `cancel`: stop the current job. Idempotent. A second cancel reports that the job is already stopped.
- Progress pings at a declared interval while a job runs. They are host-side heartbeats for the stall timer; they do not inject into the model and are not a wake. The model waits for the `job.finished` wake or calls `status`; it does not poll in a tight loop.
- A stall timeout: if no progress ping arrives in time, the plugin fails as `plugin_error` with the last ping and the artifact path, and does not leave a zombie job.
