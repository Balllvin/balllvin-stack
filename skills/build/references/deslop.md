---
name: deslop
description: Remove code that fails a slop test, and clean a branch diff. Use when cleaning a branch diff, reviewing generated code, or the user says deslop / remove slop / clean up AI code. A slop call names the failed test, the file, and the line.
---

# Remove code slop

Check the diff against main. Remove what fails a test below. Prefer the file's existing voice over a new house style.

This is a filter, not a rewrite mandate. Keep guards and structure the surrounding code already uses. Delete unnecessary code comments. Exceptions: license headers, tool directives with a reason, shebangs, and generated files. If ponytail or thermo-nuclear asks for a deeper structural change, do that instead of cosmetic cleanup alone. Never trade product speed for a cleaner shape.

`code-quality.md` owns the policy. The test names here match that reference.

## What counts

Correct, fast enough, and cheap to run is the bar. Formal guarantees stay expensive, so velocity is allowed when tests and observability show the behavior. "Slop" is not a review comment by itself. Use the word only when you name which test fails, with file and line:

1. **Unnecessary complexity from a bad abstraction.** A second way, a wrapper, a pass-through, or a type that hides the data. Separate that from necessary complexity, which is the domain's real behavior and failure modes. [Radical simplification](radical-simplification/index.md).
2. **A miss of this repo's conventions.** The diff breaks the file's patterns or this repo's rules: layers, error shapes, names, `AGENTS.md`.
3. **A test that restates calls, constants, or branches and stays green when the behavior breaks.** [Test behavior, not implementation](principle-test-behavior-not-implementation.md) and the revert check in [tests](tests.md).
4. **A change a reviewer cannot explain from the diff and the PR body.** The reader cannot say what the change does, where the data comes from, and how it fails. [Minimize reader load](principle-minimize-reader-load.md).
5. **A failure mode the code hides.** The failure cannot be named from a type, a test, an assertion, or a log.

Taste is not a test. When you compare diffs, cite added and deleted from `git diff --numstat`.

## Where attention goes

Spend the review on three boundaries. Implementation in the middle can stay pragmatic when these hold:

1. **Intent.** The spec, the done-when line, and the PR's plain-words explanation name the behavior.
2. **Architecture.** Module boundaries, data shapes, and migrations, before code inside a module. Do not delete one unless the diff says what later change gets cheaper. A review of code inside a module names an effect on speed, correctness, or what a user sees, or it is dropped.
3. **Invariants as checks.** Types, contracts, property tests, behavior tests, assertions, and observability. A boundary with no mechanical check is a wish.

Slop in the middle is tolerable when intent, architecture, and invariants each have a mechanical check. Prefer deletion and reuse (the build ladder), and keep one slice's diff small.

## Focus areas

### Comments and narration
- Extra comments that restate the next line, narrate "what" instead of "why", section banners (`// ===== Helpers =====`), emoji in comments, and changelog comments
- Docstrings that duplicate the function name without adding contracts, units, or failure modes
- Workarounds belong in the PR description or an issue, never in a comment

### Defensive theater
- Defensive checks or try/catch blocks that are abnormal for trusted / already-validated code paths
- Catch-log-and-continue that swallows errors the caller should see (hand off real silence bugs to `silent-failure-hunter`)
- Null/empty guards that cannot fire given upstream types or invariants

### Types and indirection
- Casts to `any` / `as unknown as` used only to bypass type issues
- Thin wrappers, pass-through helpers, or single-implementation interfaces added "for clarity"
- Optional fields and silent fallbacks that paper over an unclear boundary

### Structure and style
- Deeply nested code that should be simplified with early returns
- Speculative abstractions, feature flags, or config for values that never change
- Verbose names that fight local conventions (`dataValueResult`, `handleClickEventHandler`)
- Import or formatting churn unrelated to the change
- Other patterns inconsistent with the file and surrounding codebase

### Tests and fixtures
- Tests that only assert mocks were called, with no behavior contract
- Tests that walk the same branches as the implementation and stay green if behavior breaks
- Fixtures full of `"John Doe"`, `"Acme"`, `99.99%`, or emoji unless the product surface truly needs them
- Snapshot or golden updates that bury accidental copy/UI slop instead of fixing the source

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites. Deletion over reformatting.
- Do not restyle unrelated files or "while I'm here" cleanup outside the diff.
- Do not delete a real failure mode to make a file look simpler.
- If a structural code-judo move is obvious and in-scope, prefer it; otherwise leave a short note and stop.
- Keep the final summary concise (1-3 sentences): which tests failed, what was removed, what was left on purpose.

## See also

- `ponytail` when the failure is speculative abstraction or a re-implement of an existing helper.
- `thermo-nuclear-code-quality-review` when the failure is spaghetti growth, thin wrappers, or a file-size gate.
- `silent-failure-hunter` when the failure is swallowed errors or success-looking failure paths.
- `ui-ux` / `taste-skill` when the diff is UI chrome, not code style.

## Credit

Distilled from the October 2026 thread (Lauren Tan `@poteto` and Andrei Maxim `@rockatanescu`, plus contributors on necessary complexity, boundaries, tests/observability, and architecture cost).
