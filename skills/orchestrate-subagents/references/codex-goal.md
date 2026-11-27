---
name: codex-goal
description: Run a durable goal-pursuit loop for complex work. Use when asked to keep iterating until an objective is complete, finish a multi-step task end to end, maintain progress across turns, work from a durable objective, track evidence and remaining work, avoid premature completion, or continue autonomously until complete, blocked, paused, or budget-limited.
---

# Codex Goal

Turn a user objective into a durable execution loop: keep a compact goal state, choose the next concrete action from that state, verify progress with evidence, and continue until the objective is actually complete or genuinely blocked.

Do not treat the goal as a plan to discuss. Treat it as the active success criterion for the thread.

## Goal State

Maintain a compact goal state while working:

```text
Goal State:
- objective: <single concrete finished state>
- status: active | paused | blocked | budget_limited | complete
- success_criteria:
  - <observable requirement>
- evidence:
  - <completed proof, file, command output, artifact, or decision>
- remaining:
  - <unfinished requirement or verification>
- blockers:
  - <decision/access/risk, or none>
- budget:
  - <turn/time/token/resource limit if provided, otherwise none>
```

Keep this state short and useful. Update it after meaningful progress, before compaction or handoff, when blocked, and before claiming completion. Do not expose it every turn unless it helps the user or future continuity.

## Form The Objective

Before executing, convert the user's request into one concrete objective:

1. Identify the finished artifact or outcome.
2. Extract required behavior, scope, constraints, tests, docs, UI expectations, and non-goals.
3. Convert ambiguous language into observable success criteria.
4. Record anything that cannot be decided safely as a blocker.
5. Start immediately when the next action is clear.

Good objective shape:

```text
Deliver <outcome> in <scope>. Include <required behavior/docs/tests>. Verify with <checks>. Stop when <observable completion state>.
```

If the user provided enough context to choose a safe interpretation, make that interpretation and proceed. Ask only when ambiguity would change the product direction, risk profile, data access, or destructive action.

## Execution Loop

While status is `active`:

1. Pick the highest-leverage remaining requirement.
2. Inspect the real current state before changing it.
3. Make the smallest complete change that moves the goal forward.
4. Verify the change with the most relevant available evidence.
5. Update goal state: evidence gained, remaining work, blockers, and status.
6. Continue without waiting for the user when the next step is within scope.

Do not stop at planning when implementation or verification is possible. Do not present partial progress as completion. Do not repeat work unless evidence is missing or stale. Do not create broad abstractions unless they directly improve the path to the objective.

## Evidence Discipline

Prefer concrete evidence:
- file paths and changed behavior
- command output, tests, builds, linters, type checks, or browser checks
- screenshots or inspected UI state
- generated artifacts and their location
- PR, issue, or review state
- explicit user decisions

Passing tests are useful only if they cover the requirement; a checklist is useful only if every item maps to real evidence. If a verifier cannot run, record why and use the best available substitute.

## Completion Audit

Before setting status to `complete`, run a completion audit:

1. Restate the objective as concrete deliverables.
2. Map every explicit requirement to evidence.
3. Inspect the actual artifact, code, output, or state.
4. Run or cite relevant verification.
5. Identify missing, weakly verified, or uncovered requirements.
6. Continue working if anything material is incomplete or uncertain.

Only call the goal complete when every success criterion is satisfied and no required work remains. If completion is impossible without user input, set status to `blocked` and ask for the exact missing decision, artifact, access, or permission.

## Continuation

If the work spans turns or context boundaries, preserve the goal state in the response (`objective`, `status`, `evidence`, `remaining`, `blockers`). On resume, rebuild context from the saved goal state and real artifacts, trusting evidence only after verifying it still applies.

## Pausing And Blocking

Pause or block only for real reasons: user asks to pause; missing required credentials/files/decisions; destructive or production-affecting action without approval; remaining work exceeds scope; verification blocked with no substitute. Provide the smallest exact ask that unblocks progress.

## Budget Handling

If given a budget, prioritize requirements proving completion, keep exploration narrow, keep goal state compact, and avoid cosmetic work. If exhausted before completion, set status to `budget_limited`, summarize evidence, remaining work, blockers, and next action. Never mark complete because time or tokens ran out.

## Final Response

When complete: `status: complete`, concise summary of changes, verification performed, residual risk or unavailable checks. When not complete: current status, useful progress and evidence, exact remaining work, exact blocker or next action.
