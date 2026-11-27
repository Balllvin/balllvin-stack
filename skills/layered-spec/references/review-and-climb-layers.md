# Review layers, benches, ports, hill climbs, dependencies and state machines

Every plan with more than three build layers gets review layers. Every rewrite runs bench, then port, then climb. `check-slices.py` enforces the cadence, the lenses, the bench link, the climb lines, and the dependency line.

## Slice kinds

A slice may carry a `Kind:` line. The default is `build`.

| Kind | What it does | Ownership |
|---|---|---|
| `build` | Ships part of the product | Strict: no Owns overlap inside the layer |
| `review` | Runs, checks and fixes what earlier layers shipped | Loose inside a review layer |
| `climb` | Moves one measured production or fixture number | Loose inside a review layer, strict inside a build layer |
| `bench` | Only measures: records a dated baseline for code a later slice will port | Loose inside a review layer, strict elsewhere |
| `port` | Rewrites code in another language or framework and must beat its bench | Strict |

A review layer holds only `review`, `climb`, and `bench` slices. Never mix in a `build` or `port` slice. A layer of only `bench` slices does not count toward the review cadence.

## Review layers and lenses

After every two or three build layers, insert one review layer. `check-slices.py` fails a plan with four build layers in a row.

Each slice in a review layer has one job, runs in parallel with its siblings, and fixes what it finds. A review slice proves each fix with a command, test, or measurement, never just a diff reread.

Every review slice carries a `Lens:` line:

| Lens | Loads | Deterministic first pass | Job |
|---|---|---|---|
| `full-tests` | `audit/references/full-tests.md` | every app's suite, backend first | Fix what is wrong; never skip, loosen or delete a test |
| `silent-failures` | `audit/references/silent-failure-hunter.md` | swallow scan across error paths | Narrow every swallowed or disguised error and show an honest state |
| `test-quality` | `audit/references/pr-test-analyzer.md` | tautology and disabled-test scan | Delete tests that cannot fail, add tests that go red on revert |
| `type-design` | `audit/references/type-design-analyzer.md` | compiler, clippy, `tsc --strict` | Make illegal states unrepresentable at added boundaries |
| `thermo-nuclear` | `audit/references/thermo-nuclear-code-quality-review.md` | duplication and file-size check | Deep modules, no god files, no copies, nothing over 500 lines |
| `performance` | `audit/references/performance-profiler.md` | the plan's bench scripts | Find the cost, prove it, fix it, report the number |
| `security` | `security/SKILL.md` | the security skill's scans | Auth, keys, money, untrusted input, dependencies |
| `ui-polish` | `audit/references/ui-polish.md` | width, touch, and Slow 3G matrix | Fix what looks broken, with before and after screenshots |
| `formal-verification` | `audit/references/formal-verification.md` | state machine / transition scan | Model-check state machines and locks with TLA+ and canaries |
| `port-proof` | `build/references/port-proof.md` | replay and byte-compare tool | Re-run proof on every merged port from clean |
| `area` | `audit/SKILL.md` Diff review | the area's focused tests | Own one area earlier layers touched and fix it directly |

Every review layer includes `full-tests`, plus the lenses matching what earlier layers changed. Because review siblings may overlap, each review slice gets its own branch and PR, merged sequentially with rebase and focused recheck.

## Bench, port, climb

Every rewrite runs in three steps across layers:

1. **Bench (`Kind: bench`).** Records a dated baseline (`p50_ms`, `p95_ms`, `peak_rss_mb`, `cold_start_ms`, `bytes_shipped`) on redacted recorded inputs or local fixture servers. `Measures:` names the metrics; redaction strips secrets, tokens, emails, and account IDs.
2. **Port (`Kind: port`, `Bench: <bench slice id>`).** Follows `build/references/port-proof.md`: byte-compare parity, 10+ new inputs, canary break, and must beat the bench by at least 2x (targeting 10x).
3. **Climb (`Kind: climb`, `Rubric:`, `Baseline:`).** Moves one target metric via locked-check hill-climbing (see `build/references/poteto-mode/playbooks/hillclimb.md`, adapted from Bil0000/Hill-Climb MIT). Keep a step only when a locked check scores it better and all regression guards stay green; confirm with a 3-run median.

## Dependencies and languages

- Every slice owning a manifest or lockfile carries a `Dependencies:` line (what it removes, or what it adds and why in-house code cannot do it).
- Keep dependency counts moving down; remove replaced packages and update lockfiles in the same slice.
- Memory-unsafe first-party code requires a measured 2x+ win over safe alternatives and strict process/FFI isolation.

## State machines

Plans touching stateful UI or multi-step flows name explicit `*_TRANSITIONS` tables, test illegal transitions alongside happy paths, and pair critical concurrency/lease tables with TLA+ model checks (`formal-verify`).

## Writing them into the plan

- Number review layers like any other layer.
- A review layer's slices still carry label, `Size:`, Owns, Forbidden, Depends/Needs, Done when, Written against, STOP if.
- On `Schedule: needs-graph`, review, climb, and bench slices are not exempt from Owns overlap; overlap is allowed only along a `Needs:` edge (a review slice owns the report/test it writes, not the tree it reads).
