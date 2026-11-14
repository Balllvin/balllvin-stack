---
name: bounty-sizing
description: >-
  Use when sizing a bounty run: pick the short or deep workflow, and a
  reasoning-effort tier, from difficulty signals.
---
# Bounty workflow by difficulty

Use when a hunter finds a bounty, or a coordinator needs to size a run, and you must pick short vs deep plus a reasoning-effort tier.

## Inputs (required)

- Issue URL
- Amount (a fact only)
- Acceptance criteria (quoted or linked)
- Swarm signal (comment count, open PRs, "don't open new PRs")
- Stack fit

## Gate first

Skip, or escalate to the project owner, if any of these are true:

- Not funded, or the amount is unknown
- A claim farm or a multi-day swarm, unless the project owner has already said yes
- The maintainer said don't open PRs
- Not day-scope for the quoted payout

## Difficulty score (quick)

Add 1 for each true:

- Repro is unclear, or needs environment archaeology
- Touches more than two packages, or auth / session
- No existing tests near the change
- Swarm (many claimers or open attempts)
- Acceptance is vague

| Score | Label | Workflow | Effort |
|------:|-------|----------|--------|
| 0–1 | easy | short | medium |
| 2–3 | default | short | high |
| 4+ | deep | deep | highest on approach only; implement and review stay high |

Also force deep if any signal from the bounty-workflow-authoring skill fires (large payout, security / auth / migrations, many files, contested, needs a plan debate).

## Output

One line to the implementer and the hunter:

`DIFFICULTY=<easy|default|deep> EFFORT=<medium|high|highest> WORKFLOW=<short|deep> REASON=<short>`

Then run the bounty-factory skill with that workflow.
