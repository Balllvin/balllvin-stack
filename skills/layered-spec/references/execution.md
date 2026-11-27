# Execution formats

Every plan can run three ways. The spec does not pick one for good: it carries everything each way needs, and the person who starts the run picks by how many slices are left.

## Pick the format

Count the slices left: every slice whose status in `## Implementation table` (or `layers.md`) is not `merged`. `check-slices.py` prints the count and the format when you pass it the spec file (or split parts).

| Slices left | Format | Prompt |
|---|---|---|
| More than 15 | Heavy orchestrator | [orchestrator-heavy.md](orchestrator-heavy.md) |
| 15 or fewer | Light orchestrator | [orchestrator-light.md](orchestrator-light.md) |
| Any count | Manual, when the owner wants it | [manual-prompts.md](manual-prompts.md) |

Offer manual in every reply, one line under the recommended prompt. The cutoff is 15 and only 15. A plan that drops to 15 slices left mid-run may switch to the light prompt for the remaining layers; nothing else changes.

## What every format shares

- The same slices, labels, Owns lines, Done-when lines, and layers.
- Every slice carries a difficulty label (`easy`, `easy-ui`, `hard`, `hard-ui`) on its heading and its `Size:` line, and an `Owns:` line of exact backticked paths. `check-slices.py` fails a slice without them.
- No two slices in one layer share an Owns path. In orchestrated formats this keeps parallel agents in one worktree from colliding. A plan marked `Schedule: needs-graph` is the exception in [orchestrator-needs-graph](orchestrator-needs-graph.md): a slice starts when its `Needs:` ids have merged, and shared files require a `Needs:` edge.
- **No `Model:` line on a slice and no hardcoded model names anywhere in the spec or prompts.** Difficulty labels govern rigor, checklist depth, UI proof, and `/audit` critic scope, while every orchestrator and subagent runs on the caller's configured default model (`inherit-parent`).
- Every slice runs `/audit` review waves on its diff before finishing, using its label's critic scope (stop after wave 1 only when clean; otherwise run at least three waves until zero critical, high, or medium findings and at most two low nits).
- Per-job compute accounting in PR bodies and `## Implementation table`.
- The house rules below, word for word, in every prompt.

| | Manual | Heavy orchestrator | Light orchestrator |
|---|---|---|---|
| Who starts slice agents | Owner, one paste per slice | One general orchestrator agent | One general orchestrator agent |
| Branch | One per slice, from the slice's `Branch:` line | One per layer, `<agent>/<BRANCH_PREFIX>-l<N>` | One per layer, same name |
| PR | One draft PR per slice | One draft PR per layer | One PR per layer |
| Models | Caller's configured default model (`inherit-parent`) | Caller's configured default model (`inherit-parent`) | Caller's configured default model (`inherit-parent`) |
| Review | Each slice runs its label's `/audit` review waves | Per-slice `/audit` review waves plus one layer wave of three reviewers | Per-slice `/audit` review waves plus subagent layer review |
| Who merges | Owner | The orchestrator, per layer | The orchestrator, per layer |
| Final step | None beyond the write-back slice | Full review, fix forward, release notes and a release name | Same |

## Per-job compute accounting

Every slice records four wall-clock phase numbers in minutes in its PR body and in its row of `## Implementation table` (`Slice | Label | Job | Status | PR | Est | Actual | Variance | Why`):

- Estimate per phase (`read`, `build`, `test`, `audit waves`) written before the first edit.
- Actual per phase (`read`, `build`, `test`, `audit waves`) recorded at completion.
- Total `Est`, `Actual`, and `Variance`.
- A one-line `Why` explaining any variance above 25%.

## Execution section template

```markdown
## Execution

<TOTAL> slices in <LAYER_COUNT> layers: <COUNTS_BY_LABEL>. Slices left: <LEFT>. Recommended format: <heavy orchestrator | light orchestrator> (more than 15 left runs heavy; 15 or fewer runs light). Manual stays available at any count.

Prompts, house rules, and `## Implementation table` live in `<SPEC_PATH>` (or `<PROMPTS_PATH>` and `<LAYERS_PATH>` when split). Only the orchestrator (or, in manual runs, each slice's builder for its own row) edits the implementation table.

- Manual. Owner types `Implement <SLICE_ID>: ` and pastes the block for that slice's label from `## Prompts`. Each slice gets its own branch and draft PR, runs `/audit` review waves, logs compute, and updates its table row. Owner merges.
- Heavy orchestrator. One general agent on the caller's default model gets the heavy prompt. Per layer it opens one branch `<agent>/<BRANCH_PREFIX>-l<N>` from fresh `origin/main`, one shared worktree and one draft layer PR linking this plan PR, runs every slice of the layer at once using its label prompt block, runs one layer review wave of three reviewers, applies fixes, merges the layer PR and marks the rows merged with actual compute.
- Light orchestrator. One general agent gets the light prompt and uses subagents on the caller's default model to build, review and merge each remaining layer the same way.

<GATES: any check that must pass between two layers, with its exact commands, or "No gates between layers.">

House rules for every agent in every format: see `## House rules`. This plan PR is never merged or marked ready.
```

## Prompts layout template

Default to putting `## House rules` and `## Prompts` directly inside `product-specs/<slug>.md` so the spec stays self-contained in one file. Only split into `product-specs/<slug>.prompts.md` and `layers.md` for mega-ports or `Schedule: needs-graph`. Fill every plan placeholder once the plan PR exists, and never bake a slice id or a model name into any template or manual paste.

## House rules

Copy this list into every prompt. Do not paraphrase it.

```text
- Focused tests for changed files are enough. Never run slow full-repo CI from a build slice unless coordinating an explicit Full Tests / Full CI pass.
- No unnecessary code comments.
- Never revert. Fix forward.
- Never deploy by hand or change production environment variables or secrets from a build slice.
- Work on your own until everything is done. Every question carries a default answer: act on the default and list it under "Defaults taken".
- No destructive stored-row changes, backfills, or money/order execution without explicit owner approval.
- Never skip, xfail, or loosen a test, and never lengthen its timeout.
- No raw provider error, URL, or HTTP status code reaches a person on any surface.
- Never merge or mark ready a plan PR.
- Never invent facts. Label anything unverified.
- Unslop every PR body, comment, and commit message.
If something needs the owner (a secret, money, a stored-row change), finish everything around it, take the safe default, list it under "Needs owner", and keep going. Never stop to wait.
```
