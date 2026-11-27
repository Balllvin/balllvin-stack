# Code quality

Ponytail after tracing the real flow: delete, reuse, stdlib/native, then the minimum. No speculative abstractions or parallel homes for one concept.

**Slop is a failed test, not a label.** Name which test in [deslop](deslop.md) fails, with file and line. The five tests are:
1. Unnecessary complexity from a bad abstraction.
2. A miss of the repo's conventions.
3. A test that restates calls, constants, or branches and stays green when the behavior breaks.
4. A change a reviewer cannot explain from the diff and the PR body.
5. A failure mode the code hides.

Leave taste aside. Review module boundaries, data shapes, and migrations before code inside a module. A review of code inside a module names an effect on speed, correctness, or what a user sees, or it is dropped. Never trade product speed for a cleaner shape. Clean something up when it changes speed, correctness, what a user sees, or the cost of a later change the diff names. When `git diff --numstat` added lines exceed deleted lines by 100 or more, the PR states added, deleted, and why the addition is the minimum. If the PR states a decision, that decision is in the diff, a lesson, or the spec.

## DRY and deep modules

Code must be DRY. When the same constant, type, validation, or block of logic appears in more than one place, move it to one shared owner and reuse it. A literal repeated three or more times in one product file gets a named constant because the name carries intent. DRY the owners and the structure, not every similar line: two call sites that only look alike stay separate until they change together.

Prefer deep modules: a small interface over a lot of behavior. Apply the deletion test before adding a layer: if deleting a module only moves its few lines into its callers, it is a pass-through and should go. One adapter behind an interface is a guessed seam, so inline it. Two real adapters make a real seam. Start refactors at the hot spots: files that change most often (`git log --format= --name-only | sort | uniq -c | sort -rn | head`) and are hardest to read.

Routes orchestrate. Services decide. Clients transport. Components render. Shared code stays generic. Finish cross-boundary changes in one PR, including callers, empty/error states, and tests.

## File size, comments, and dependencies

Hand-written product and test files: **350 lines** is healthy, **500** is the hard split line, **1000** is stop. Split by responsibility, not line chunks. Generated, vendored, and immutable migrations are exceptions. A narrow production or security repair may defer a split only when doing it now increases risk: state why, and do not grow the file. Working code that worsens structure does not ship.

Do not write tautology comments that repeat the code, or excuse comments on a hack; fix the code instead. Express how the code works through names, types, small functions, and tests. Keep comments only for non-obvious invariants or outside constraints the code cannot show (or move workarounds to the PR description/issue). Allowed exceptions: license headers, tool directives (`eslint-disable`, `type: ignore`, `noqa`, `pragma`, `@ts-expect-error`) **with a reason**, shebangs, and generated files.

No dates in file, DB, function, or tool names. No unrelated file changes. No new runtime dependency without a written technical justification in your dependency budget; dependency counts only go down.

Never cap an agent tool loop with a turn budget, round cap, `max_turns`, or remaining wall-clock budget. The model runs until it stops; each individual provider call may use a fixed hang timeout.

## Database and structured logging

- Keep durable deployed state in one primary relational store (for example PostgreSQL). Avoid introducing an extra general cache until metrics prove a narrow bottleneck that read models, provider caches, and payload trimming cannot solve.
- Hot routes serve warm read models or cached rows with freshness metadata, then enqueue refresh rather than fanning out to external providers before first paint. Speed work must expose `stale`/`degraded`, never hide failures.
- Leave structured logs a future reader needs to reconstruct what a feature did. Put operation IDs on events as fields (`request_id`, `run_id`, `job`, `tool`, `user_id` when safe) and log at boundaries: start, decision, failure, done.
- Keep levels honest: `error` for real failures, `warning`/`info` for expected skips. Never log secrets, tokens, cookies, auth headers, or raw request bodies; sanitize third-party error text before logging or display. No silent `except` on a user path.
