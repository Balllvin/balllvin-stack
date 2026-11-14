---
name: bounty-workflow-authoring
description: >-
  Use when picking or writing a bounty workflow (short vs deep) for a funded,
  claimable issue, using difficulty signals.
---
# Author bounty workflow

Keep two standing bounty workflows. Never invent a third per issue.

| Workflow | When |
| --- | --- |
| short | Default day-scope work in a familiar stack, under a modest payout |
| deep | Any difficulty signal below fires |

## Difficulty: go deep if any one is true

- Payout is large, or the payout rail is unclear
- Likely more than a handful of files, or an unknown public API surface
- Security, auth, migrations, money, or data-loss risk
- Needs a short debate of two or three plans before coding
- A prior failed attempt, or a contested issue (a swarm of "just try it" agents is a skip, not a deep run)

If none fire, use short.

## Reasoning effort

- **medium** — triage, mechanical edits, test runner, still-open checks
- **high** — default implement, plus a separate review agent
- **highest** — deep approach, large blast radius, or security only

Never use highest on every child task. Cap the agent budget.

## Workflow authoring

- Declare metadata first: name, description, and phase titles. Use the same phase names every time: `problem`, `approach`, `implement`, `real-test`, `review`, `ship`.
- An agent call returns a structured result. Read the output field. Don't treat the whole result as a string.
- Prefer a typed output schema and booleans over string-contains checks or brittle templates.
- Capability mode: read-only for problem, approach, and review; read-write for implement; execute for real-test.
- Pause for missing arguments or a human gate. Use a terminal complete state when the run is done.
- Deep means short, plus a parallel approach phase, plus a second implement pass. Not a huge fan-out of dozens of agents.

## Steps

1. Confirm the issue is open, funded, and claimable. Not a farm, not a swarm.
2. Score difficulty and pick short or deep.
3. Start the coding harness with the model your router already chose.
4. Pass the issue URL, the amount as a fact, and the acceptance criteria.
5. The real-test phase must log the commands it ran, or the run fails closed.
6. Pause before a public claim or PR. Hand off to whoever owns shipping and payout collection.

## Refuse

- Wiring this bounty path into a product whose model broker is locked, unless the owner changes that product
- Calling a run "tested" without command logs
- A third standing workflow
- A 40-to-80 call fan-out
