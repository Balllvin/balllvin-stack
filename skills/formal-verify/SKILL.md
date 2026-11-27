---
name: formal-verify
description: >-
  Model-check state-machine, concurrency, lock, and lease races with TLA+ and
  TLC, and exhaustively verify small pure policy gates. Use when a change
  touches state transition tables, run leases, fencing tokens, distributed
  locks, retry or recovery loops, or pure decision gates. Triggers:
  /formal-verify, "model-check", "TLA+", "TLC", "lease fence", "stale write",
  "state machine", "canary".
---

# Formal verify

A unit test checks the order of steps someone thought of. TLC checks every order of steps in a small bounded model. Each spec in `formal/` models one subsystem, names its promises as invariants, and carries an anti-vacuity canary: one constant that switches on a known break, so a passing run is never vacuous.

## Does your change touch it?

Maintain a `formal/coverage.json` manifest that lists, per spec, the source files and symbols it models plus `synced`, the commit at which someone last confirmed the spec describes that code. Run your spec gate whenever a branch changes any covered file or adds a new writer to covered state columns (for example, status or `lease_*` columns on a run table, or session phase fields).

## Run

Run the TLA+ model checker via your project's pinned runner with the canary check enabled:

```sh
# Single spec with canary verification
<formal-runner> --spec <SpecName> --canary
# Full formal suite with expected spec count
<formal-runner> --all --canary
# Canary and regression harness
node --test formal/tests/test_canary.ts
```

Keep TLC and the pinned JRE cached locally outside the repository tree. A canary harness (`test_canary.ts`) checks that each invariant fails on a broken variant of the code it guards and that every known open finding still reproduces.

## Read a result

Read every trace with a statechart view so each counterexample prints as the shortest path in code terms.

Then replay the counterexample against the real code, one step per model action, as a focused integration test on the repository or service functions:

- If the path cannot happen in the real code, the model is wrong until you prove otherwise: tighten the model so each action maps 1:1 to one transaction or atomic step in the code.
- If the path does happen, it is a real finding. Never weaken an invariant or the model to go green. Record it under Known findings in `formal/README.md` with a constant that reproduces it, add a case to `test_canary.ts`, and let the cfg check the remaining behavior with that one path gated behind the finding constant until product code is fixed.

## When the code changes on purpose

Update the model step that maps to the changed code, rerun the spec with its canary (`Canary = FALSE` in the nominal cfg, and `Canary = TRUE` failing as expected), and fix any `test_canary.ts` edit whose source text moved. Advance `synced` in `formal/coverage.json` only after reading the covered code at the new commit and confirming the spec describes it. Transition-table changes and spec copies must land in the same change.

## Adding a spec

1. Add one `.tla` and one `.cfg` in `formal/`, with `Canary = FALSE` exactly once in the cfg.
2. Add its `formal/coverage.json` entry (files, symbols, `synced` commit) and its rows in `formal/README.md`.
3. Add one `test_canary.ts` case per property proving the spec catches a planted break (anti-vacuity).
4. Update your CI/gate spec count if your runner enforces `--expect-specs`.

## Pure policy gates and property tests

- **Pure gates over small inputs:** When a policy gate is a pure decision over a few small discrete inputs, enumerate every input combination exhaustively against an exact specification instead of sampling.
- **Data-integrity and concurrency:** Pair TLA+ design checks with seeded property tests (`proptest` in Rust, Hypothesis-style generated inputs in Python) and at least one planted mutant in your mutation suite so the test suite proves it catches a real break.

## Worked pattern: fenced lease

For a worker run leased to one turn at a time:
- Each claim increments `lease_epoch` and mints a fresh `lease_token`.
- Every write passes through a single fence predicate checking `(lease_owner, lease_epoch, lease_token)` and active status (`status == "active"`). Checking `lease_owner` alone fails when the same worker reclaims a timed-out run and an older turn still holds the previous token.
- Key invariants to model: `OneLiveClaim` (at most one turn passes the fence at any step), `NoStaleWrite` (writes only land from the newest lease), `NoWriteAfterStop` (cancellation blocks further writes), `OneOutcome` (terminal states cannot be overwritten), and `StatusFollowsTable` (every transition matches the single `*_TRANSITIONS` table).
- Canary break: drop `lease_epoch` and `lease_token` from the fence predicate and confirm TLC emits a counterexample violating `OneLiveClaim` and `NoStaleWrite`, then replay that exact interleaving in a repository unit test.
