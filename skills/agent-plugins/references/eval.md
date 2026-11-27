# Eval

Every plugin ships a small held-out eval: tasks the author did not use while writing the card or the self-test. The eval measures whether the wording and the loop work in the agent's hands, not whether the self-test passes.

## Shape

- A handful of tasks (start with five if you can, three if the job is narrow). Each task has a starting workspace, a prompt, and a checkable outcome (green tests, a typed `work_failed` at a known file, a rejected invalid action, an input-check failure).
- Hold them out. If you tuned the card on one of these tasks, move that task to the smoke set and add a fresh held-out task.
- Run the eval **three times** on the same plugin version and the same harness version. The spread of the three scores is the **noise floor**. A later change "wins" only if it clears that floor, not if it wins one run by a point.
- If the spread is huge, the eval is measuring luck or a flaky setup. Tighten the task, not the prompt, first.

## Grading

- The grader checks both the end state and what the agent told the user. A mismatch scores zero.
- A known shortcut (hard-coded output, peeking at the check, skipping the wake) scores zero.
- Every card, manifest, or loop change records its predicted score movement and a falsifier. No falsifier means no ship.
- Run lightly changed held-out copies (filename case, one flipped requirement, a renamed artifact). Passing originals while failing copies means overfitting.
- `plugin_error` counts as Invalid and is excluded from the `work_failed` rate.

## Run logs

Every eval run and production job records:

- the plugin id and pinned plugin version
- the harness id and pinned version
- the job id and retry key
- the outcome (`ok`, `work_failed`, `plugin_error`) and typed failure lines when any
- the duration and whether the stall timer fired

Without pinned versions a later comparison is meaningless.

## What not to do

- Do not treat the self-test as the eval. The self-test is a gate on promote; the eval is a held-out measure of the plugin in the agent's hands.
- Do not tune the card on the same tasks you report as the held-out score.
- Do not compare two plugin versions across different harness pins and call the delta an improvement.
