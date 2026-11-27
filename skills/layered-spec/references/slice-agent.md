# Slice-agent template

The orchestrator sends this to one subagent per slice, in both orchestrated formats, on the caller's configured default model (`inherit-parent`). It fills `<SLICE_ID>`, `<LAYER_BRANCH>`, `<LAYER_PR>`, `<LAYER_WORKTREE>` and `<SLICE_FILE_N>` (`<SPEC_PATH>` for single-file specs). Then it appends the block for the slice's label.

Manual runs do not use this file. They use [manual-prompts.md](manual-prompts.md), where each slice gets its own branch and PR.

```text
Implement <SLICE_ID> on layer branch <LAYER_BRANCH> (layer PR <LAYER_PR>) in the shared layer worktree <LAYER_WORKTREE>.
Core goal: your slice is done when proven. Every Done-when line has its proof, `/audit` review waves are clean, phase compute is logged, and only the files in your Owns line are committed to <LAYER_BRANCH>.
Read AGENTS.md. Find <SLICE_ID> in <SLICE_FILE_N> on the plan branch <PLAN_BRANCH> (plan PR <PLAN_PR_URL>). Read <SPEC_PATH> and any spec section the slice names. Never build on, edit, or merge the plan branch.
Before you edit, confirm the slice's Written against SHA still matches the cited excerpts. If a STOP if condition holds, that step stops; report Found: and do the rest of the slice that is still valid.
Before your first edit, record your estimated compute minutes per phase (`read`, `build`, `test`, `audit waves`).
Setup: work only in <LAYER_WORKTREE>, which the orchestrator set up on <LAYER_BRANCH>. Never create a worktree or a branch. Every other slice agent of your layer edits and commits in this same worktree at the same time, so: stage and commit only your Owns paths by name (git commit --only -- <paths>), never git add -A or git add ., and never push, pull, rebase, stash, reset, checkout, or switch. If .git/index.lock exists, wait a few seconds and retry. Never touch a file outside your Owns line, even to fix a test run that another agent's half-done file breaks; note it under "Not mine" and rerun later. Your slice text may name another slice of your layer, but its code is not there yet. Never import it.
Finish the slice. Do not end your turn with a question. Decide reversible things, note the choice under "Changed from the spec", and keep going. Only secrets, money, stored-row changes, or keychains go under "Needs owner", each with the default you took. Do the rest around them.
Files: build inside Owns. If an Owns path is wrong, take the obvious reading, report it under "Found", and continue. A red test that also fails on origin/main, or that does not touch your slice, is one line under "Not mine". Any other red test that touches your slice is yours. If the code is wrong, fix the code. If a test outside Owns is wrong or out of date, report it under "Found" for the reviewers instead of editing it.
Checks: run only your slice's focused tests and the test files in Owns. The main change has a test that fails when reverted.
Rules: never edit lessons/, lessons.md, or AGENTS.md unless your slice owns them; write a lesson under "Lesson" in your summary. Do not open a PR, mark anything ready, or merge. The orchestrator does that.
<HOUSE_RULES>
Hygiene: commit after each finished step with `git commit --only -- <your paths>`. Before your last message stop your servers and watchers and drop scratch databases. Leave the shared worktree in place; the orchestrator removes it after the layer merges.
Compute: at the end, record actual minutes per phase (`read`, `build`, `test`, `audit waves`), total Est, total Actual, variance, and a one-line Why if variance exceeds 25%.
Report: your last message is the slice summary, unslopped: Slice / Commits / Implemented (each Done-when line with its proof) / Not implemented (reason) / Changed from the spec / Found / Needs owner / Checks / Not mine / Audit waves (findings per wave) / Compute (Est/Actual per phase, variance, why) / Lesson. Before and after samples go here for easy-ui and hard-ui slices.
```

## Easy block

```text
This slice is easy: a clear target in named files, no design. Trace callers and make the small choices inside your files yourself. No screen or message text changes. Run /build deslop on your diff, then run /audit review waves (bug, quality, ponytail, and reuse critics): stop after wave 1 only if wave 1 is clean, otherwise run at least 3 waves and keep going until a wave has zero critical, high, or medium findings and at most 2 low nits, fixing verified findings between waves.
```

## Easy-ui block

```text
This slice is easy-ui: a clear target that changes what a person reads (message text, a field, a state, a button) on any surface. Do everything in the easy block (and run the UI/UX critic on every /audit review wave alongside the bug, quality, ponytail, and reuse critics). Load /ui-ux and follow its message rules and unslop.md. Keep the layout and add golden-text tests for every message. Put before and after samples for every surface you change in your slice summary: golden text for messages, screenshots at 390x844 and desktop for screens.
```

## Hard block

```text
This slice is hard. Read README.md, lessons.md, and the spec sections the slice names. Trace the real flow and list every caller before you edit. Load the slice's Skills. Run the /build blast-radius check before cross-cutting edits, and /security when the slice touches auth, keys, money, or untrusted input. Name the one remaining way in a sentence and make the tree match it. Where a later layer fills a slot, leave a stub that fails loud. Run /build deslop on your diff, then run /audit review waves (all five critics in wave 1; later waves re-run every critic that found something): stop after wave 1 only if wave 1 is clean, otherwise run at least 3 waves and keep going until a wave has zero critical, high, or medium findings and at most 2 low nits, fixing verified findings between waves. Report bugs or spec errors anywhere under "Found".
```

## Hard-ui block

```text
This slice is hard-ui. Do everything in the hard block. Load /ui-ux and the UI architecture doc of each app you touch. Message text is UI. Walk the current screens or messages first. Ship end to end on every surface the slice names, with empty, loading, stale, and failed states for screens and golden-text tests for messages. Prove flows with Playwright or native/SSR render tests, with screenshots at 390x844 and desktop. Never sign in with the owner's real tokens; use test fixtures. On `/audit` review waves, run all five critics plus the UI/UX critic in wave 1, and include the UI/UX critic in every subsequent wave until a wave has zero critical, high, or medium findings and at most 2 low nits (minimum 3 waves unless wave 1 is clean). Put before and after samples per surface in your slice summary.
```
