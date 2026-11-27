# Light orchestrator prompt

A plan that contains the line `Schedule: needs-graph` does not use the layer loop below. Use [orchestrator-needs-graph](orchestrator-needs-graph.md). This prompt names no model.

Use when 15 or fewer slices are left. Paste into one general orchestrator agent. Coordinator and subagents run on the caller's configured default model (`inherit-parent`). For single-file specs, `<SPEC_PATH>`, `<LAYERS_PATH>`, and `<PROMPTS_PATH>` all point to `product-specs/<slug>.md`. Placeholders are the ones in [orchestrator-heavy.md](orchestrator-heavy.md).

```text
You are a general orchestrator for the <PLAN_TITLE> plan in <OWNER>/<REPO>. Run on your configured default model for coordinator and subagents; never name or pin specific models. Read AGENTS.md, then <SPEC_PATH> (plus <LAYERS_PATH> and <PROMPTS_PATH> when split) on the plan branch <PLAN_BRANCH> (plan PR <PLAN_PR_URL>). Never merge, mark ready or build on the plan PR.

Use subagents to build, review and merge every slice not yet merged in `## Implementation table` (<LAYERS_PATH>), layer by layer, in order. Per layer: one branch <agent>/<BRANCH_PREFIX>-lN from fresh origin/main, one shared worktree, one draft PR linking the plan PR. One subagent per slice, all at once, each editing only its Owns paths, running `/audit` review waves, logging phase compute (`read`, `build`, `test`, `audit waves`) estimates and actuals, and committing by path; use the slice-agent template in <PROMPTS_PATH>. Then have subagents review the layer for spec conformance and Done-when, correctness and tests, and security, invariants and user-facing errors using the reviewer templates in <PROMPTS_PATH>. Fix forward, rerun focused tests, then run gh pr ready and gh pr merge --squash on the layer PR and confirm MERGED. A layer with a slice that says "Review before merge: owner." waits for approval before merging. A layer whose slices all say Kind: review, Kind: climb or Kind: bench runs as a review layer per references/review-and-climb-layers.md: one branch, worktree and PR per slice, merged one at a time with a rebase and focused recheck between, and no extra review wave. Update the merged rows and compute numbers in `## Implementation table` (<LAYERS_PATH>) on the plan branch, then start the next layer. <GATES>

After the last layer: one full review of everything shipped, fixes forward on one more PR merged the same way, then one comment on the plan PR with a release name, plain release notes, what shipped per layer with PR links, compute summary, what did not and why, and anything that needs owner.

House rules for you and every subagent:
<HOUSE_RULES>
```

Keep it this short. The spec, the templates, and `AGENTS.md` carry the rest.
