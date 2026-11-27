# Review slice ownership and effort

Read this before locking or changing Layer 6. `/build` owns implementation; this check makes the handoff runnable.

## Label by the work, not its name or line count

Use `easy` for an exact mechanical target with an existing public keeper and no unresolved design. Use `hard` for semantic, cross-owner, concurrency, transaction, security, freshness, or compatibility decisions, or a full rewrite on a daily path. Add `-ui` (`easy-ui`, `hard-ui`) whenever a person reads the output, on any surface; message text is UI. These four are the only labels.

A small diff can be hard. A large mechanical deletion can be easy once caller absence, every deleted path, and the surviving contract are proved. Record the label and its reason on the slice's `Size:` line. Keep UI classification tied to the actual edited behavior, not a read-only component citation.

## Make every owner executable

- For a typed result cut, trace the callback or protocol signature through every producer, consumer, and direct test/fixture binding. Reserve the definition and affected bindings in Owns before dispatch.
- Trace tests through public route, CLI, and MCP dispatchers. Direct-import searches miss generic entrypoint callers. Follow compatibility facades to the live owner before assigning paths.
- Enumerate every file to delete, every caller test/fake that must change, and any reserved new path. A count such as "delete 32 pages" is not an Owns list.
- Keep evidence-only paths read-only. Citing a canonical cache, shared source verifier, or schema does not authorize editing it.
- Give shared CI, generators, lockfiles, and schema revisions to exactly one slice per layer. If more slices need one, move them to the next layer. Never route them to a "parent queue".
- Require a count, result, absence check, or benchmark that fails on reversion. "Is clean" and "no slop" are not Done-when lines (`build/references/tests.md`).
- When a helper replaces repeated work, reserve proof at the caller that invokes it. Helper-output parity proves the result, not fewer invocations.
- Name the exact focused command for every owned proof, including a reserved test path if created.
- Run only the slice's focused tests and the test files in Owns (never slow full-repo CI from a build slice). A red test that does not touch the slice or also fails on `origin/main` gets one line under `Not mine` and does not block `Merge-ready: yes`. Any other red test touching the slice is the builder's.

## Recheck published assignments

Fetch current `origin/main` before dispatch and integration. If another merge removed or relocated the target, record the resolving PR, immutable `main` SHA, and boundary proof rather than widening Owns or creating an empty PR.

If a keeper disproves the proposed cut, withdraw the finding with failure evidence rather than adding features just to make deletion safe.

## Keep the map readable

Within each layer, assign letters A through Z, then AA onward, in the order slices appear across sorted slice files. Letters are display order, not a dependency or performance rank.

Run `python3 <skills-dir>/layered-spec/scripts/check-slices.py <slice-parts...>` for exact path collisions, missing contracts, invalid labels, `Size:` mismatches, `Model:` bans, and letter order. Inspect policy-sensitive ownership yourself; a parser cannot decide whether two files share a transaction or schema head.

## Report deletion honestly

Sum exact deduplicated removal ranges, separately for production and tests. Label gross removable lines, replacement estimates, and expected net reduction separately. Exclude aliases, conditional findings, retained cases, and overlapping estimates.
