# Tests

Every new or changed test passes the `/audit` test gate (`../../audit/references/test-audit.md`): name the behavior it protects, the regression that breaks it, why existing tests miss it, and whether it needs a production seam only tests use. A missing answer means do not add it.

- A test your change breaks is yours to fix, wherever it lives. If the contract changed, retarget the assertion. If the product is wrong, fix the product. A red test is not an automatic revert.
- Legitimate: new contract, moved owner, false pass/fail, missing path, decomposition that preserves collected test identity. Not legitimate: skip, xfail, loosen, raise a timeout, hide the failure in a mock, or delete an unrelated red test to go green.
- **Revert-proof.** Each main change has a test that fails when the change is reverted. Watch it fail once on a scratch revert. A test that restates calls, constants, or branches and stays green when the behavior breaks does not satisfy this rule.
- **Concurrency, distributed systems, money, and data-integrity changes** include a property test, an idempotency test, or a reconcile check. UI glue does not need that stronger check.
- **Seeded property tests & planted mutants.** Use deterministic seeded property suites (`PROPERTY_SEED` / `proptest`) and verify each suite against at least one planted mutant in your mutation harness so tests prove they catch real bugs.
- **Exhaustive enumeration for pure policy gates.** When a security, permission, or financial policy gate is a pure decision over a few small discrete inputs, enumerate **every combination** against an exact specification instead of sampling.
- Patch the owner or pass `now`, the session, or the client in. Do not patch private helpers (`_utcnow`) through a facade, and do not copy a facade's globals into split modules so old patches keep working.
- Shared fixtures and fakes live in `conftest.py` or a `*_support` module. When production calls a new method, extend the shared fake once.
- No copied lists in tests (route tables, `__all__`, re-export identity, line caps). Generate the list and verify with `--check`.
- Read source as text only to guard bytes that ship (prompts, Dockerfile, migrations, public exports). Never grep source text to prove a deleted identifier stays deleted.
- A PR that deletes code deletes the tests that only covered it.
- Name test files after the code they test, not after a plan step or wave.
- Run focused tests for the files you changed rather than re-running slow whole-repo CI suites unless explicitly asked.

## Done means

Before you say a task is done, all of these hold. If one does not, say which at the top of your report:

1. Every Done-when or acceptance line is met, each with the test or command that proves it.
2. `/audit` test-audit "Before you say done" holds: revert-proof tests, nothing skipped or loosened, no test-only seams.
3. The focused tests for this change passed, and you named the exact commands. Never call a new red test "pre-existing".
4. `deslop` ran on the diff. Non-trivial diffs also ran `/audit` thermos or review waves.
5. The PR body explains the change in plain words, what was not done and why, and whether it is ready to merge.
