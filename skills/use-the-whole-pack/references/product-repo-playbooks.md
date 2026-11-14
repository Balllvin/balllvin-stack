# Practice pack for a product repo

Default entry for any non-trivial coding task in the repo this skill is attached to. Read the operating-mode skill and the matched playbook before writing a plan.

## Start

1. Open a todolist. First item: read the operating-mode principles index.
2. Match a playbook and copy its steps in verbatim as todos. A skipped step stays in the list with `skip: ` and a one-line reason.
3. Stay in this repo. Cloud agents use the model and effort from the router. Don't let a setup script overwrite it.

## Playbooks

- Investigation: read-only how/why. Cited answer, no PR.
- Bug fix: reproduce on the matching surface, binary-search the cause, smallest evidence-backed fix, failing check before the fix when cheap (tdd).
- Feature: how, then architect if it crosses a boundary, name the data shape, throughput checkpoint, an implementer writes the code, you review the diff, prove it on the real surface, opening-a-pr.
- Refactoring: pin behavior first, subtract before add, migrate callers then delete, prove equivalence, revert if reader load did not drop.
- Babysit: declare mode first (`drive` / `check` / `threads-only` / `background`). Frontier PR only. Order: conflicts, then threads, then CI. Stop at merge-ready. Do not merge.
- Shipping: only when the owner asks to land. Independent verify first. Propose the merge. Do not arm auto-merge unless they say so.
- Opening a PR: end of every code playbook. Voice first, then unslop the PR text. Deslop the diff. No-comments before review. Small PRs. Propose before consequential merges.

If none fit, use figure-it-out. Large cross-cutting work goes there too.

## Skills to fire as needed

- how: walk the subsystem before changing it.
- why: evidence-cited motivation (git always; name skipped source categories).
- architect: sketch types and signatures before code that crosses a function boundary. At least two shapes. Scrap the sketch if implementation keeps fighting it.
- tdd: failing cheap local test first on bug fixes. Skip with a reason when the test path is expensive.
- interrogate: adversarial review of contested design or a ship-ready diff. Two independent passes, then lead judgment. Do not auto-apply.
- blast-radius: prove the one safety fact by running code, not a writeup.
- no-comments: strip narrating comments before review. Keep only a non-obvious why.
- language practices: any edit in that language.
- unslop: every draft that leaves. Voice first, then how-to-write (sentence), then how-to-write-paragraphs if longer than about four sentences. No skip. PR copy, commits, notes.
- technical-writing: docs, RFCs, readmes, then the writing stack.
- create-verification-skill: only when the repo has no scripted way to prove a user path and the next feature needs it.

## Hard rules

- Name the data shape before writing logic.
- Smallest change that solves it. Delete first.
- Verify against the real artifact. "It compiles" is not done.
- Can I simplify this? on every implement and every text.
- Voice first. Then how-to-write. Then paragraphs on anything longer than four sentences. Do not swap a tell for a cousin. Do not fake humanity with slang or typos.
- Propose before merges and deploys.
- Ping the coordinator only on blockers.
