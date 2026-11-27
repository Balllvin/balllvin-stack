# Formal verification

Use when a promise in the code can break in an order of steps or an input that tests rarely reach: concurrency, retries, claims and locks, schedulers, state machines, parsers, and `unsafe` Rust. Tests check the cases someone wrote. A model checker checks every order of steps inside a stated bound. See `../../formal-verify/SKILL.md` for the full model-checking workflow.

## Pick the target

1. Inventory state machines and split lifecycles (`*_TRANSITIONS` tables or paired status/timestamp flags).
2. Pick the promise where a break hurts users most and tests reach least: an order or job proposed twice, a run lost on restart, a claim held by two workers, money moved on stale state.
3. Name the property in one plain sentence and the harm in another.

## Pick the tool

- Bad orders of steps: TLA+ with TLC over a small bounded model of the design.
- Every input to one function: property tests on the real code (`proptest` in Rust, Hypothesis-style generated inputs in Python), exhaustive combination enumeration for small pure policy gates, or Kani for `unsafe` Rust.
- A property that must hold at every size: a proof, only when a bound is not enough.

## What makes it count

- Every model step points to code a reviewer can open. One atomic step in the model is one atomic step in the code.
- **Anti-vacuity canary:** The check fails on purpose first. Break the guarded code on a scratch change (drop a check, reorder two steps) and show the counterexample. A check never seen failing proves nothing.
- A finding stays a finding. Report the counterexample as steps in the code's words. Never weaken the property or the model to pass.
- State the bounds and what the model leaves out.
- One command reruns it in under two minutes, with the tool version pinned.
- Record the covered files/functions and the `synced` commit in `formal/coverage.json` and the PR body.

## Output

```text
Property: <one sentence>
Harm if broken: <one sentence>
Tool and bounds: <tool, version, bounds>
Result: pass | counterexample <steps in code words>
Proved it can fail: <the scratch break and the counterexample it produced>
Covers: <files, functions, commit>
Rerun: <command>
```

Adapted from pstack `create-formal-verification-skill` by Lauren Tan (MIT). See `../../THIRD_PARTY_NOTICES.md`.
