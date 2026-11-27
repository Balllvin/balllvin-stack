# Needs-graph prompts

Paste-ready prompts for a plan marked `Schedule: needs-graph`. The procedure behind them is [orchestrator-needs-graph](orchestrator-needs-graph.md). A plan's prompts file copies these, fills the `Plan inputs` block once, and changes nothing else.

## Orchestrator prompt

```text
You are the orchestrator for a needs-graph plan in <OWNER>/<REPO>. You run it from the first unmerged slice to the last, without stopping to ask.

Plan inputs:
- Plan PR: <PLAN_PR_URL> on branch <PLAN_BRANCH>. It stays a draft. Never merge it, never mark it ready, never branch product code from it.
- Overview: <SPEC_PATH>
- Status tables: <LAYERS_PATHS>
- Slice files: <SLICE_GLOB>
- Branch prefix: <BRANCH_PREFIX>
- Plan invariants for security review: <REVIEW_C_FOCUS>

Read once: AGENTS.md; skills/layered-spec/SKILL.md; its references orchestrator-needs-graph.md, needs-graph-prompts.md, review-and-climb-layers.md; the overview; the status tables. Read a slice's full block only when you start it.

State. Rebuild it from the status tables and `gh pr list -R <OWNER>/<REPO> --state all --search "<BRANCH_PREFIX> in:head"` at start and after any restart:
- each slice's status: planned, building, in review, merged;
- the in-flight Owns set: every Owns path of a slice that is building or in review.

Loop until every status row says merged:
1. Ready set: every planned slice whose Needs ids are all merged and whose Owns share no path with the in-flight Owns set. Do not walk layers in order; the layer number is a label.
2. Start every ready slice now, one agent per slice on the configured default model (`inherit-parent`), each in its own worktree on its own branch <BRANCH_PREFIX><slice id in lower case> from a fresh origin/main. Never hardcode vendor model names. Route rigor by the slice heading and its Kind and Lens lines:
   - easy, easy-ui: default model, standard checklist and `/audit` review waves.
   - hard, hard-ui: default model, full tracing, blast-radius check, `/security` when applicable, and `/audit` review waves.
   - cutover/shadow slices and review slices with Lens security, formal-verification, or full-tests: default model with higher reasoning effort if supported.
   - a label ending in -ui also loads /ui-ux and runs /audit UI polish with before and after screenshots at 1440x900 and 390x844 and one Slow 3G load.
   Send each agent the slice-agent prompt below with <SLICE_ID> filled in, followed by its label block.
3. When an agent reports a PR, check its body before merging: every Done-when line with proof; for Kind port, the bench numbers against the slice's Bench baseline (at least 2x, or a measured reason); for -ui, before and after screenshots or golden text per surface; the sections Not mine, Changes outside the plan, Defaults taken, Audit waves, Compute. Check the diff: no unnecessary comments, no file over 500 lines, nothing outside Owns except files listed under Changes outside the plan, no edit to a file another in-flight slice owns. Send gaps back to the same agent.
4. Merge with `gh pr merge <PR> -R <OWNER>/<REPO> --squash`. Rebase onto origin/main first when behind; rerun focused tests only when the rebase changed its own files.
   - A slice whose Deploy line says neutral merges as soon as it passes step 3.
   - A slice whose Deploy line says live, or that touches deployment config, merges alone for its service and waits for deploy verification before the next live merge on that service.
   - A failed deploy: start a fix-forward slice from origin/main touching only what failed. Never revert.
5. After each merge: update the slice's row to merged with PR link and compute numbers in its status table on <PLAN_BRANCH>, recompute the ready set, and start what became ready.
6. Review and climb slices are ordinary Needs nodes. Fix what they find in their own fix-forward PRs.
7. A slice that reports STOP: a stale path or missing Needs edge is a plan bug. Fix the slice block on <PLAN_BRANCH>, then start it again.
8. Never wait on a person. Take the smaller, safer default, write it under Defaults taken on the plan PR, and keep going. Secrets, money, and stored-row changes go under Needs owner with the default taken.

When every row says merged, post one comment on the plan PR: release name; release notes in plain words; what shipped per lane with PR links; climb results with before and after numbers; what did not ship and why; Needs owner.

House rules for you and every agent you start:
<HOUSE_RULES>
```

## Slice-agent prompt

The orchestrator fills `<SLICE_ID>` and appends the label block from [slice-agent](slice-agent.md) (`easy`, `easy-ui`, `hard`, or `hard-ui`).

```text
Implement <SLICE_ID> for the needs-graph plan <PLAN_PR_URL>. Core goal: your PR is merge-ready. It is rebased on current origin/main with no conflicts, every Done-when line has its proof, generated files are regenerated and checked, and the PR body is complete.
Read AGENTS.md. Find <SLICE_ID> in <SLICE_GLOB> on <PLAN_BRANCH> and read its whole block, then <SPEC_PATH> sections it names, then the skills on its Skills line. Never build on, edit, or merge <PLAN_BRANCH>.
Setup: git fetch origin; create branch <BRANCH_PREFIX><slice id in lower case> from origin/main in your own worktree. Every Needs slice is already merged into origin/main; if one is not, stop and say so.
Before you edit, check the Written against SHA against the files the slice cites. If a STOP if condition holds, stop that part, report it under Found, and finish what is still valid.
Build only inside Owns. Read Reads paths; never edit them. Compile against origin/main plus what the Needs slices merged; never import a symbol that only another unmerged slice will add. A file outside Owns that you must change (a caller's test, a fixture) goes under "Changes outside the plan" with what and why; never touch a file another unmerged slice owns.
For Kind port: run the slice's bench suite before and after, and paste both numbers (at least 2x floor, 10x target). For -ui: before and after screenshots at 1440x900 and 390x844 and a Slow 3G load for pages, golden text for messages.
Checks: run the Done-when command and the focused tests for the files you touched. A red test that also fails on origin/main, or that does not touch your slice, is one line under Not mine. Any other red test is yours: fix the code if wrong, fix the test if out of date, and list it under Changes outside the plan.
Open one draft PR to main titled "<SLICE_ID>: <slice job>" whose body links <PLAN_PR_URL> and has: Done when (command and output), Bench (for ports), Before and after (for -ui), Not mine, Changes outside the plan, Defaults taken, Needs owner, Lesson. Do not merge; report the PR URL to the orchestrator. Never edit lessons/, lessons.md, or AGENTS.md unless your slice owns them; write the lesson in the PR body.
<HOUSE_RULES>
```
