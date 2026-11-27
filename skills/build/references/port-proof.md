# Port proof

Load for any slice that rewrites working code in another language or framework: Python to Rust, React to server-rendered HTML, JavaScript to TypeScript, a package to in-house code. A port fails quietly. It passes the tests someone wrote and differs on the inputs nobody tried. The proof comes from evidence a script checks, never from a model's opinion.

## Before the port

1. **Bench first.** Record the old code's dated baseline: p50 and p95 ms, throughput, peak memory, cold start, and bytes shipped on redacted recorded inputs or local fixture servers.
2. **Extract the rules.** List each business decision the old code makes as a Given/When/Then line with its `file:line`. Mark the ones where a wrong answer hurts users or money as P0.
3. **Record real inputs.** Capture real requests, rows, and messages once into fixtures. Add broken and edge inputs.

## The proof

The port is proven only when all of these hold. Run them from a clean build:

- **Tests ran.** The full focused suite runs from clean and its counts come from the runner's own output. A run that executed no tests fails.
- **Same inputs, same outputs.** Old and new run on the same recorded inputs and a script compares every byte. Mask only fields that must vary (timestamps, generated ids), allow a stated tolerance on floats, and list every mask in the PR body.
- **New inputs.** Add at least ten inputs nobody recorded: empty, huge, boundary, unusual order, malformed. Compare again.
- **Tests can fail.** Break one line of the new code on a scratch change. The tests must go red, and the byte compare must catch a changed byte.
- **Every P0 rule has a test that ran.** A rule named only by a skipped test is not proven.
- **Speed beats the bench.** Target 10x the bench baseline on the same rubric, with 2x as the floor. Keep iterating on the new code (profile, cut allocations, cut round trips, batch, cache) until it reaches 10x or two rounds in a row gain nothing. Below 2x, record the external limiter (a provider round trip, a database query, network latency) with the measurement that proves it.

Each module gets one verdict in the PR body: **PROVEN**, **PARTLY PROVEN** (say what is missing), or **NOT PROVEN**. Only PROVEN switches traffic.

## After the proof

1. Switch the route or job to the new code behind the strangler router.
2. Delete the old code and its dependencies in the same slice once the switch is proven. No shim outlives its layer.
3. Lower dependency and language ratchets.
4. Keep improving the same rubric on subsequent optimization passes.

Adapted from Anthropic's `code-modernization` plugin (Apache-2.0). See `../../THIRD_PARTY_NOTICES.md`.
