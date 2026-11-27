# Lifecycle: editing a plugin in use

A plugin that is already running still has to be editable. An edit never mutates the version an active job already pinned.

## The loop

1. **Edit.** Open the current promoted version and write a draft. The draft gets a new version number. Record the reason and the author (`user` or `agent`) on that draft. The promoted version stays where it is.
2. **Validate.** Schema validation and card lint must pass. Failures fail. See [manifest](manifest.md).
3. **Self-test.** The plugin's self-test must pass on the draft. A self-test that only checks "the file exists" is not enough; it should exercise the happy path (`ok`), one `work_failed` path, and at least one `plugin_error` break.
4. **Promote.** Only a draft that passed both checks can be promoted. The previous promoted version remains available for rollback.
5. **Pin.** A job records the plugin version (and the harness version) at start and keeps it until the job ends. A promote mid-job does not change that job.
6. **Rollback.** One step: the previous promoted version becomes current again. Rollback is itself a logged edit (reason, author). You cannot roll back past version 1, and you cannot roll back a job that already pinned a later version; you can only start a new job.

When managing manifests in git before a store exists, bump `version`, pass the self-test in the same PR, and record the reason in the PR body. Never overwrite a shipped manifest without a version bump.

## Authors

`user` is a person. `agent` is a model authorized to edit that workspace or repo. The log stores the author label, a specific reason string (`"card loop named a missing action; added code.tests.cancel"`, never `"update"` or `"fix"`), the version, and the timestamp.

## Deprecation

To retire a plugin:

- Mark it deprecated in the index with one sentence naming the replacement, if any.
- Stop promoting new drafts except to fix a break.
- Keep old versions readable so a pinned job and a run log can still explain what happened.
- Do not delete a version that a stored run still points at.

A rename is a new plugin id plus deprecation of the old one (and a redirect entry if callers still invoke the old tool name).

## What the model sees

The discovery index lists promoted plugins only, plus a draft the current author is editing. A job in flight does not switch cards mid-run when a draft is promoted.
