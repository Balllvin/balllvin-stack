# Untangle

Adapted from [untangle-codebase](https://github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md) (caldoai, MIT).

One question for every piece of code: **should these pieces change together?** Every problem below is a place the code answers it wrong. Scope by app path, never the repo root.

## 1. Measure

Run deterministic checks first so you spend reading time on design problems rather than mechanical greps:

- **Mechanical ratchet checks:** Scan the diff or area for copied blocks and constants, pass-through wrappers, swallowed errors, sleeps and retry loops, disabled tests, tests that cannot fail (`assert True`, `x == x`, empty test bodies, `expect(x).toBe(x)`), and **silenced checks** (`# type: ignore`, `# noqa`, `@ts-expect-error`, `eslint-disable`, `as any`). Fail when changed files add new silenced checks or tautology tests.
- **Import and caller map:** Trace who imports what, the tests that cover each file, and unused exports/dead code.
- **State lifecycle map:** Hunt single lifecycles split across several boolean/string flags instead of one explicit `*_TRANSITIONS` table.

## 2. List every problem

Change nothing yet. Write each one down as `path:line` and one sentence:

- **Hidden links**, must change together but nothing shows it: copied logic or values, a module reading a global or file another module sets, one feature split across folders by layer, a call order callers just have to know.
- **Needless links**, tied together but change for different reasons: callers reaching into internals, stable code importing volatile code, a general function with a parameter only one caller understands, a shallow module whose interface moves with its internals.
- **Surplus**, no reason of its own to change: pass-through wrappers, config or extension points nothing varies, dead code.
- **Special cases**: an `if` for one value, a parameter for one caller, a swallowed exception, a retry or sleep, a disabled test, a silenced type or lint check. Each is a requirement the design missed; use them to work out what the design needs.

`git log --format= --name-only -- <area>` shows what actually changes together.

## 3. Redesign, then fix

Find the one fix behind several problems ([redesign from first principles](../../build/references/principle-redesign-from-first-principles.md)). Write the decision log as fixes, each with the problems it solves nested under it, and put it in the PR body. Pieces that change together end up together, pieces that don't are not tied, and everything depends on what changes less.

Fix the whole list, special cases through the redesign rather than one by one. Keep behavior the same apart from bugs the redesign fixes, and prove it with existing tests plus the Tests lens (`test-audit.md`). Comments follow `../../build/references/no-comments.md`.

Done when a typical change lands in one place, no import points at something more volatile, silenced-check and duplication counts for the area went down, and a second pass finds nothing worth fixing.
