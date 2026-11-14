---
name: bounty-factory
description: >-
  Use when shipping funded, claimable bounties through a repeatable coding
  harness (problem, approach, implement, real-test, review, ship).
---
# Bounty factory

Use when someone hands you a funded, claimable issue and you need a repeatable path to a shippable PR. Prefer a standing harness over a one-off chat.

## Standing setup

- Harness and model come from the coding router, not from a model id typed in this skill.
- Coding owner implements. Hunt owner finds and claims. Project owner coordinates payout and blockers.
- Never commit secrets. Never invent bounty amounts.

## Invoke

From the bounty repo, start the harness the router already chose, then run the short or deep workflow with:

- issue URL
- amount (a fact only)
- acceptance criteria (quoted or linked)

## Phases (keep these names)

1. **problem** — Fact: the issue is open and claimable, you can reproduce it, and acceptance is clear. Don't promote a guess to a fact.
2. **approach** — Smallest slice, blast radius, and the commands that will prove it. Deep runs 2–3 plans in parallel, then picks one.
3. **implement** — Private branch, small commits, no secrets. Deep does a second pass and does not widen the scope.
4. **real-test** — Real commands plus exit evidence. Fail closed if this phase is skipped.
5. **review** — A second agent, read-only. Approve or request changes.
6. **ship** — Pause before a public claim or PR. The hunt owner collects. Escalate to the project owner on merge-to-collect problems, or to the human on blockers.

## Short vs deep

Pick with the bounty-workflow-authoring or bounty-sizing skill.

- **short** — Day-scope, crisp acceptance.
- **deep** — Short, plus approach fan-out, plus a second implement. Highest reasoning effort only on approach or security.

## Reasoning effort

- medium — triage, mechanical work, test runner
- high — default implement and review
- highest — deep approach, large blast radius, or security only (rare)
