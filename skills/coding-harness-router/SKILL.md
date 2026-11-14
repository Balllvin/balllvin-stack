---
name: coding-harness-router
description: >-
  Use when starting paid or product coding: a router picks the model, then
  the installed practice-pack skills and the matching playbook run the work.
---
# Coding harness router

Use when a coding run starts. A router picks the model from config. The installed practice pack is how the work is done. Read the skill file. Do not work from memory.

House skill: apply the practice pack. Bakeoff, coverage fan-out, orchestration, autopilot, and a measured improvement loop are in scope. Apply every installed skill that can apply. A skill that cannot apply is a named disagreement, not a silent skip.

## Model router

| Layer | Choice |
| --- | --- |
| Default harness | The local or CLI harness your config names |
| Model | The coding-family default from config, not a model string hard-coded here |
| Auth | Whatever the harness already uses. Don't paste keys into a prompt. |
| Fallback | The next model in the ordered fallback list, only when the default harness is down |
| Hosted cloud agent | Only if the local harness and its fallbacks are both dead. Use the cloud-agent id and effort from config. |

Disagreement: do not run the pack's setup skill if it would replace this router with the pack's own model defaults. The router still picks the model.

## How the work runs

Open the operating-mode skill, match one of its playbooks, open that file, and copy its steps before any task todos. A skipped step stays in the list with `skip: <reason>`. Opening a PR is the end of every code playbook.

Playbooks, all in scope: investigation, bug-fix, perf-issue, measured improvement, runtime-forensics, trace-forensics, feature, refactoring, prototype, visual-parity, authoring-a-skill, eval, babysit, shipping, autonomous-run, orchestrate, autopilot, session-pickup, pause-safely, multi-phase-plan, worktree-cleanup, then opening-a-pr.

Also apply when the task matches: architect, bakeoff, automate-me, benchmark-checklist, blast-radius, correct, create-verification-skill, figure-it-out, how, interrogate, maintain-verification-skill, no-comments, the principle skills, recall, reflect, show-me-your-work, coverage fan-out, tdd, teach, technical-writing, language practices, unslop, why.

Defaults when several fit: investigation for a read-only payable-or-not question, bug-fix for a defect, feature for new behavior, perf-issue for one measured slowness, a measured improvement loop only for a sustained metric loop, babysit for an open PR, shipping to land a green stack. Bakeoff, fan-out, orchestration, and autopilot are allowed when the task is a comparison, a coverage spread, a multi-day program, or a PR queue. Do not use them as the default for a single day-scope bounty.

## Bounty size (inside the playbook)

1. Size with bounty-sizing or bounty-workflow-authoring.
2. Run the bounty-factory skill.
3. Easy day-scope: short workflow, medium effort. A normal PR under a modest payout: short, high effort. Hard, security, multi-package, or contested: deep, high effort (highest on approach only).

Phases stay problem, approach, implement, real-test, review, ship. real-test is fail-closed. Pause before a public claim.

## Handoff line

`HARNESS=<harness> MODEL=<from-config> EFFORT=<medium|high|highest> MODE=<workflow:short|workflow:deep|goal|interactive|fallback> PLAYBOOK=<playbook name> REPO=<url> ISSUE=<url> WHY=<short>`

If a cloud agent is required, add the cloud model and effort from config.

## Out of scope

- A different product repo whose owner has not opened this path
- Parked payment-integration work
- The pack setup skill (named disagreement above)
