# Reviewer templates

One review wave per layer, three reviewers at once, running on the orchestrator's configured default model (`inherit-parent`). For single-file specs, `<SLICE_FILE_N>` is `<SPEC_PATH>`. The orchestrator fills `<LAYER_PR>`, `<LAYER_BRANCH>`, `<LAYER_WORKTREE>`, and `<SLICE_FILE_N>`, then appends one role block. For the final review it replaces the layer with the whole plan: every layer PR, every slice section, and a fresh worktree on `<agent>/<BRANCH_PREFIX>-final`.

Block C ends with `<REVIEW_C_FOCUS>`: the plan's own invariants from Global constraints and Review focus.

```text
You review layer PR <LAYER_PR> on branch <LAYER_BRANCH> for the <PLAN_TITLE> plan (plan PR <PLAN_PR_URL>). Read AGENTS.md, <SPEC_PATH> (and <SLICE_FILE_N> when split), and the slice summaries in the layer PR body. Two other reviewers run at the same time with other roles. Stay in your role.
Work in the shared layer worktree <LAYER_WORKTREE>; never create another. Fix what you can in place: commit small fixes to <LAYER_BRANCH> by path with `git commit --only -- <paths>`, never push, pull, rebase, stash, or reset, and rerun the focused tests your fix touches. The orchestrator pushes. Flag the rest with file, line, what is wrong, and the fix you propose.
Do not mark ready or merge.
<HOUSE_RULES>
Report: your last message, unslopped: Role / Fixed (commit, what) / Flagged (file, line, problem, fix) / Checked and fine / Checks you ran.
```

## Reviewer A block

```text
Role A, spec conformance and Done-when. For each slice of the layer: every Done-when line is met and its named test exists and passes; the diff stays inside the slice's Owns line, and any file outside it is explained; each part's goal and before and after are met; the label block was followed (golden text and screenshots for easy-ui and hard-ui); the merge-ready checklist items hold; the acceptance items that name this slice are covered; the slice summary includes its Audit waves findings and per-phase Compute accounting (`read`, `build`, `test`, `audit waves`). Flag any Done-when line, audit wave, or compute block claimed without proof.
```

## Reviewer B block

```text
Role B, correctness, tests, and integration. Run every focused test the layer's slices name, together, from the layer branch. Read the diff for logic bugs, missing error paths, races, and dead code. Check that the slices of the layer fit: every function one slice calls in another exists with the shape the caller uses, stubs a later layer fills fail loud, imports resolve, generated files (catalogs, mirrors, schemas) match their generators, and nothing an earlier layer shipped broke. Check that each new or changed test fails when the change it covers is reverted, and that no test was skipped, xfailed, or loosened.
```

## Reviewer C block

```text
Role C, security, invariants, and user-facing errors. Check: no raw provider error, URL, stack trace, or HTTP status code reaches a person on any surface, and every error a person sees is plain words from the owning copy module; no secret, token, or backend key reaches a client, a log, a saved message, or an agent; scoped keys never see account details; irreversible money/order actions remain unreachable or gated server-side; every route is scoped to the signed-in user; no stored-row change or backfill runs without owner approval; no production secrets changed. Run /security on any diff that touches auth, keys, money, or untrusted input. Plan invariants: <REVIEW_C_FOCUS>
```
