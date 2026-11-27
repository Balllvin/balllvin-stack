# Manual pastes

The owner orchestrates, starting one agent per slice, one at a time or a layer at a time, by typing `Implement L1A: ` and pasting the block for the slice's label. Each slice builds on its own branch (the slice's `Branch:` line) and opens its own draft PR; the owner merges.

Owns, Forbidden, Done when, and extra skills live in the spec. Single-file specs embed standalone per-label blocks under `## Prompts` (merging common rules plus the label's rules into one paste per label); multi-file splits may keep the common block plus the four label blocks below in `<slug>.prompts.md`. Replace `<SPEC_PR_URL>`, `<SPEC_PATH>`, `<LAYERS_PATH>`, and `<HOUSE_RULES>` once the plan PR exists (for single-file specs, `<LAYERS_PATH>` is `<SPEC_PATH>`). Never bake a slice id or a model name into any paste.

## Common block

```text
Core goal: this slice ends merge-ready, no matter what: rebased on current origin/main with no conflicts, tests passing, generated files regenerated and checked, PR body complete. Do not stop before that.
Read AGENTS.md. Your slice id is the token after "Implement", before the colon. Find it in <SPEC_PATH> on the plan branch (plan PR <SPEC_PR_URL>). Never build on or merge the plan branch.
Before you edit, confirm the slice's Written against SHA still matches the cited excerpts. If a STOP if condition holds, that step stops; report Found: and do the rest of the slice that is still valid.
Before your first edit, record your estimated compute minutes per phase (`read`, `build`, `test`, `audit waves`).
Setup: git fetch origin main --prune, then a new worktree on the branch the slice names from that origin/main.
Finish the slice. Do not end your turn with a question: decide reversible things, note the choice under "Changed from the spec", and keep going. Only secrets, money, stored-row changes, or keychains go under "Needs owner", each with the default you took; do the rest around them.
Files: build inside Owns. A red test that also fails on origin/main, or that does not touch your slice, is one line under "Not mine". Any other red test that touches your slice is yours even when the test file is outside Owns. If your code is wrong, fix the code. If the test is wrong or out of date, fix the test and list that file under "Changes outside the plan". Never edit a sibling's file or infer permission from a source citation.
Skills: /build on every slice; /ui-ux for the PR body and the report (words people read); /ship-verify for the gate, rebase, and PR.
Checks: run only your slice's focused tests and the test files in Owns. Never run slow full-repo CI from a build slice. Tests run once. After a later rebase rerun nothing unless the rebase changed your own files, and then only your focused tests. Never skip, xfail, loosen, or lengthen a timeout on a test. New and changed tests pass the /audit test gate, and the main change has a test that fails when reverted.
Hygiene: commit after each finished step. Wait only on your own processes. Before your final message stop your servers and watchers and drop scratch databases. Evidence goes in the PR body.
Changes outside the plan: list every file you edited outside Owns under that heading in the PR body, with what and why. Lessons: unless your slice owns lessons/, never edit lessons/ or lessons.md; write them under "## Lesson" in the PR body.
Compute: at the end, record actual minutes per phase (`read`, `build`, `test`, `audit waves`), total Est, total Actual, variance, and a one-line Why if variance exceeds 25%, in both the PR body and your row of `## Implementation table` in `<LAYERS_PATH>`.
House rules:
<HOUSE_RULES>
Report: draft PR to main linking <SPEC_PR_URL>. One comment on the plan PR, edited in place, never a second: Slice / PR / Merge-ready: yes or no, and why / Implemented (each Done-when line with its proof) / Not implemented (reason in your words) / Changed from the spec / Found / Needs owner / Checks / Not mine / Changes outside the plan / Audit waves (findings per wave) / Compute. Then update only your row in `## Implementation table` (`<LAYERS_PATH>`) on the plan branch with PR link, Est, Actual, Variance, and Why. Do not merge.
```

## Easy block

```text
This slice is easy: a clear target in named files, no design. Trace callers and make the small choices inside your files yourself. If the slice text is wrong (a file, symbol, or command does not match), take the obvious reading, post "Found:" on the plan PR, and continue. No screen or message text changes. Run /build deslop on your diff, then run /audit review waves (bug, quality, ponytail, and reuse critics): stop after wave 1 only if wave 1 is clean, otherwise run at least 3 waves and keep going until a wave has zero critical, high, or medium findings and at most 2 low nits, fixing verified findings between waves.
```

## Easy-ui block

```text
This slice is easy-ui: a clear target that changes what a person reads (message text, a field, a state, a button) on any surface. Do everything in the easy block (except run the UI/UX critic on every /audit review wave alongside the bug, quality, ponytail, and reuse critics). Load /ui-ux and follow its message rules and unslop.md; keep the layout. Add golden-text tests for every message. Put before and after samples for every surface you change in the PR body: golden text for messages, screenshots at 390x844 and desktop for screens. Add a "UI review" line to the merge-ready checklist.
```

## Hard block

```text
This slice is hard. Read README.md, lessons.md, and the spec files the slice names. Trace the real flow and list every caller before you edit. Load the slice's Skills; run the /build blast-radius check before cross-cutting edits, and /security when the slice touches auth, keys, money, or untrusted input. Name the one remaining way in a sentence and make the tree match it. Where a later layer fills a slot, leave a stub that fails loud. Run /audit review waves (all five critics in wave 1; later waves re-run every critic that found something): stop after wave 1 only if wave 1 is clean, otherwise run at least 3 waves and keep going until a wave has zero critical, high, or medium findings and at most 2 low nits, fixing verified findings between waves. Post "Found:" for bugs or spec errors anywhere.
```

## Hard-ui block

```text
This slice is hard-ui. Do everything in the hard block. Load /ui-ux and the UI architecture doc of each app you touch; message text is UI. Walk the current screens or messages first. Ship end to end on every surface the slice names, with empty, loading, stale, and failed states for screens and golden-text tests for messages. Prove flows with Playwright or native/SSR render tests at 390x844 and desktop (never sign in with the owner's real tokens; use test fixtures). On `/audit` review waves, run all five critics plus the UI/UX critic in wave 1, and include the UI/UX critic in every subsequent wave until a wave has zero critical, high, or medium findings and at most 2 low nits (minimum 3 waves unless wave 1 is clean). Put before and after samples per surface in the PR body, and add a "UI review" line in the merge-ready checklist.
```
