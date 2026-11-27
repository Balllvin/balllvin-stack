# Heavy orchestrator prompt

A plan that contains the line `Schedule: needs-graph` does not use the layer loop below. Use [orchestrator-needs-graph](orchestrator-needs-graph.md).

Use when more than 15 slices are left. Run the orchestrator, every slice agent, and every reviewer on the caller's configured default model (`inherit-parent`), never pinning vendor model names. Difficulty labels (`easy`, `easy-ui`, `hard`, `hard-ui`) govern the checklist, UI verification, and `/audit` critic scope. For single-file specs, `<SPEC_PATH>`, `<LAYERS_PATH>`, `<PROMPTS_PATH>`, and `<SLICE_FILE_N>` all point to `product-specs/<slug>.md`.

Placeholders, filled once in `## Prompts` (or `<slug>.prompts.md` when split):

| Placeholder | Example |
|---|---|
| `<OWNER>/<REPO>` | GitHub `owner/repo` |
| `<PLAN_TITLE>` | feature or migration plan name |
| `<PLAN_PR_URL>`, `<PLAN_PR_NUMBER>`, `<PLAN_BRANCH>` | the draft plan PR and its branch |
| `<SPEC_PATH>`, `<LAYERS_PATH>`, `<PROMPTS_PATH>` | `product-specs/<slug>.md` (or split files) |
| `<SLICE_FILE_N>` | `<SPEC_PATH>` when single-file, or `product-specs/<slug>.slices-lN.md` when split |
| `<BRANCH_PREFIX>` | short unique prefix; layer branches are `<agent>/<BRANCH_PREFIX>-l<N>` |
| `<FIRST_LAYER>`, `<LAST_LAYER>` | the first layer with a slice not yet merged, and the last layer |
| `<START_CONDITION>` | what must be true before L1, or `none` |
| `<GATES>` | checks between two layers, with exact commands, or `No gates between layers.` |
| `<REVIEW_C_FOCUS>` | the plan's own invariants for reviewer C |
| `<INVARIANT_FILES>` | the spec sections whose acceptance and invariants the final review checks |

```text
You are a general orchestrator for the <PLAN_TITLE> plan in <OWNER>/<REPO>. Run on your configured default model for both coordinator and subagents (inherit-parent); never pin or hardcode specific model names. Read AGENTS.md, then <SPEC_PATH>, <LAYERS_PATH>, <PROMPTS_PATH> and any split slice files on the plan branch <PLAN_BRANCH> (plan PR <PLAN_PR_URL>). The plan PR stays a draft. Never merge it, never mark it ready, never build on its branch.

Start condition: <START_CONDITION>. If it does not hold, stop and say which part is missing.

Run layers <FIRST_LAYER> to <LAST_LAYER> in order, skipping any layer whose rows in ## Implementation table (<LAYERS_PATH>) all say merged. For each layer N:
1. git fetch origin main --prune. Create the layer branch <agent>/<BRANCH_PREFIX>-lN from that origin/main, check it out in one worktree, push it, and open one draft PR to main titled "<PLAN_TITLE>, layer LN" whose body links the plan PR. This is the only worktree and the only branch for the layer. No slice agent or reviewer gets its own.
2. Start every slice of layer N at the same time, one subagent per slice on your configured default model, all working in that layer worktree. Send each the slice-agent template from <PROMPTS_PATH> with <SLICE_ID>, <LAYER_BRANCH>, <LAYER_PR>, <LAYER_WORKTREE> and N filled in, followed by the block for its label (`easy`, `easy-ui`, `hard`, or `hard-ui`). Each slice runs `/audit` review waves on its diff before finishing and records per-phase compute (`read`, `build`, `test`, `audit waves`) estimates, actuals, variance, and `Why` if variance exceeds 25%. Slice agents edit only their Owns paths, commit them by path to the layer branch, and open no PR. They never push, pull, rebase, stash, reset or switch branches.
3. Wait for every slice agent to finish, then push the layer branch. Put each slice summary and per-phase compute summary in the layer PR body. If two agents' commits conflict, the Owns lines were wrong: resolve it yourself on the layer branch and note it in the layer PR body.
4. Run one layer review wave of three reviewers on your configured default model, all at the same time, each with the reviewer template and its role block from <PROMPTS_PATH>. A checks spec conformance, Done-when lines, compute accounting, and `/audit` wave notes. B checks correctness, tests and how the slices fit together. C checks security, invariants and user-facing errors. Each reviewer fixes what it can on the layer branch and flags the rest.
5. Apply every flagged fix on the layer branch, rerun the focused tests each slice names, then push. Do not start a second layer review wave unless flagged fixes touched untested cross-slice contracts.
6. If any slice of the layer says "Review before merge: owner.", stop here, post the layer PR link on the plan PR, and wait for approval. Otherwise run gh pr ready <LAYER_PR> -R <OWNER>/<REPO> and gh pr merge <LAYER_PR> -R <OWNER>/<REPO> --squash, and confirm state says MERGED.
7. On the plan branch, set the layer's rows in `## Implementation table` (<LAYERS_PATH>) to merged with the layer PR link and Actual/Variance/Why compute numbers, commit by path and push. Remove the layer worktree with git worktree remove. Then start layer N+1. Earlier layers are never reviewed again until the final review.
Review layers run differently. When every slice of layer N says Kind: review, Kind: climb or Kind: bench, skip steps 1 to 5 and follow references/review-and-climb-layers.md: start every slice at once on your configured default model, each on its own branch <agent>/<BRANCH_PREFIX>-lN-<letter> in its own worktree from the same fresh origin/main. Merge them one at a time under step 6, rebasing the next PR on the new main and rerunning its focused checks first. Then do step 7 with every PR link.

<GATES>

After the last layer merges:
1. Run one full review of everything the layer PRs shipped, against the acceptance in <SPEC_PATH> and the invariants in <INVARIANT_FILES>. Use the three reviewer templates once more on your configured default model, over the whole plan instead of one layer.
2. Fix forward on one branch <agent>/<BRANCH_PREFIX>-final from a fresh origin/main. Open a draft PR, then ready, squash merge and confirm MERGED the same way as a layer. Skip the branch if the review found nothing.
3. Post one comment on the plan PR: a release name for the whole release; release notes in plain words; what shipped per layer with each layer PR link; total actual vs estimated compute; what did not ship and why; anything under Needs owner.

House rules for you and every agent you start:
<HOUSE_RULES>
```
