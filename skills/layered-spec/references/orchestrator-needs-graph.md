# Needs-graph schedule

One plan may opt in by putting this line in any of its files:

```text
Schedule: needs-graph
```

Every other plan keeps the layer barrier in `SKILL.md`. Do not copy this schedule into a plan that did not ask for it.

## What the checker changes

- Each slice has `Needs:`. The value is `none` or a comma-separated list of slice ids. Prose such as "all earlier layers merged" fails.
- A slice may start when every id in that list is merged, even if other slices in its layer are not.
- Same-layer `Needs` is allowed.
- `Depends:` is optional. If both lines are present, they list the same ids.
- Letter order is checked inside each file, not across files. One file may hold several layers of one product area.
- An Owns path may appear in two slices only when one can reach the other through `Needs:`, including a chain. That check includes review, climb, and bench slices. A review slice owns the report it writes, not the tree it reads.
- Review cadence, lenses, bench-before-port, manifest `Dependencies:`, and the four labels stay as they are.

## How an orchestrator runs it

Read `Needs:` and the status table. Do not walk layers in order.

A slice is ready when its status is not merged, every `Needs` id is merged, and no slice that is building or in review owns one of its paths.

Each ready slice gets its own branch `<agent>/<prefix>-<id>` from current `origin/main`, its own worktree, and its own draft PR to `main`. It commits only its Owns paths, compiles against `origin/main` plus symbols introduced by its merged `Needs` slices, and never imports symbols from another unmerged slice.

Rigor routing uses the caller's configured default model (`inherit-parent`) without pinning vendor model names:

| Slice | Rigor & reasoning effort |
|---|---|
| `easy`, `easy-ui` | Default model, standard checklist and `/audit` review waves |
| `hard`, `hard-ui` | Default model, full tracing, blast-radius check, `/security` when applicable, and `/audit` review waves |
| Cutover or shadow slices; review with `Lens: security`, `formal-verification`, or `full-tests` | Default model, deeper verification and higher reasoning effort if supported by the harness |

A `-ui` label also loads `/ui-ux` and runs `/audit` UI polish with before and after screenshots at `1440x900` and `390x844`, plus a Slow 3G load. No slice carries a `Model:` line and no prompt names a vendor model.

Build in parallel. Merge one PR at a time per deployed service (`Deploy: live` or touching deployment config waits for the merge's deploy check before the next live merge on that service; `Deploy: neutral` merges immediately once checks pass). A failed deploy is fixed by a fix-forward PR; never revert.

The paste-ready prompts are in [needs-graph-prompts](needs-graph-prompts.md). Keep going until every status row says `merged`. Never merge or mark ready the plan PR.
