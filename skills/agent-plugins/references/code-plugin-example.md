# Worked example: `code.tests`

The job: run the repo tests in the workspace, wake when the run finishes, edit every failing file named in the typed failures, rerun, and stop when everything is green. That is one done-condition, so it is one plugin. There is no `fix` action; ordinary file tools fix the code.

## Manifest

```yaml
id: code.tests
title: Code tests
version: 1
when: Run the repo tests, wake when they finish, and fix until every test is green.
entrypoint: ./index.mjs
self_test: ./self_test.mjs
actions:
  - name: code.tests.run
    description: Start the test command in this workspace and return a job id.
    timeout_s: 1200
    dry_run: false
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
        retry_key: { type: string, description: "Wake idempotency key, code.tests:<job_id>." }
        artifact: { type: string, description: Path for the test-results table once written. }
  - name: code.tests.status
    description: Read the latest job for this plugin. Use after a wake or to check a job id.
    read_only: true
    args:
      job_id:
        type: string
        description: Job id from code.tests.run. Omit to use the latest job in state.
    result:
      type: object
      additionalProperties: false
      required: [ok, kind]
      properties:
        ok: { type: boolean }
        kind: { type: string, enum: [ok, work_failed, plugin_error] }
        status: { type: string, enum: [queued, running, passed, failed, cancelled] }
        job_id: { type: string }
        failures:
          type: array
          items: { type: string }
          description: Typed failures as file:line:reason. Empty when green or still running.
        artifact: { type: string }
  - name: code.tests.cancel
    description: Stop the current test job. Safe to call twice.
    idempotency_key: "code.tests.cancel:${job_id}"
    args:
      job_id:
        type: string
        description: Job id to stop. Omit to cancel the latest running job.
    result:
      type: object
      additionalProperties: false
      required: [ok, kind]
      properties:
        ok: { type: boolean }
        kind: { type: string, enum: [ok, work_failed, plugin_error] }
        status: { type: string, enum: [cancelled, passed, failed] }
        job_id: { type: string }
  - name: code.tests.validate
    description: Check the test command and workspace without starting a run.
    read_only: true
    dry_run: true
    args:
      command:
        type: string
        description: Command to check. Omit to use the workspace setting or autodetect.
    result:
      type: object
      additionalProperties: false
      required: [ok, kind]
      properties:
        ok: { type: boolean }
        kind: { type: string, enum: [ok, plugin_error] }
        command: { type: string }
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

## Card loop (hand-written)

This text lives in a sibling `card-loop.md`, not in the YAML:

```text
Validate the command if you are unsure it will start: code.tests.validate.
Start a run with code.tests.run. If the run is still going when this turn ends, wait for the wake. Do not poll in a tight loop.
When woken, or when the run finishes in this session, call code.tests.status.
If kind is work_failed, edit the failing files named in the typed failures (use ordinary file tools; this plugin has no fix action), then call code.tests.run again.
If kind is plugin_error, report the typed failure and stop. Do not treat it as a test failure.
If you must abandon a run, call code.tests.cancel.
Done when: every row in the test-results artifact is passed, or status is passed.
```

The linter checks that every named action exists in the manifest, a `Done when:` line is present, and the loop stays under 40 lines.
