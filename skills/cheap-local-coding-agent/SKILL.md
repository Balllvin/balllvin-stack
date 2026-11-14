---
name: cheap-local-coding-agent
description: Use when your main cloud coding agent is out of quota or too expensive for the job, and you run a local CLI coding agent on a cheaper model instead. Covers the implement-then-review pair, picking reasoning effort per task, scheduling check-ins because local agents don't wake themselves, and fallbacks.
---

# Cheap local coding agent: implement, then review

When the hosted agent's quota runs out, or the job is small enough that it isn't worth it, run a local CLI coding agent against a cheaper model. Cheap tokens make a second reviewer almost free, so always use one.

## Before you start

- Read the model's data terms. Free or preview models often keep prompts and completions. Don't send secrets, customer data, or private code you can't share under those terms.
- Wrap the CLI in a small script that pins the model and reasoning effort, so every run is reproducible and nobody types a model id by hand.

## Reasoning effort

Set it per task:

- **medium**: chores, mechanical edits, tiny unblockers.
- **high**: the default. Most PRs, auth, UI, normal bugs.
- **highest**: only hard problems or changes with a large blast radius.

Don't spend max effort on a one-line fix, and don't under-think a session or auth bug.

## Workflow

1. Give one agent a small, clear slice. It implements and opens a draft PR.
2. Start a second agent as reviewer with the diff, the intent, and the tests. Review is the default, not an extra.
3. Schedule a check-in the same turn. A local agent doesn't wake itself up or report back, so set a finite timer to check its output.
4. When you stop an agent, kill it by exact process id. Never pattern-kill (`pkill -f name`), because the pattern can match your own shell.

## Fallbacks

Keep an ordered list of two or three models in the wrapper: the default, a named fallback if it's down, and a last resort only if both are down. Note why each is in the list, and move back to the default when it returns.

- Don't reach for a random other model first. Use the list, in order.
- Don't silently swap to a cheaper sibling of the same model family. Change the list on purpose, or not at all.
- On the fallback, keep reasoning effort at **high** by default; the same medium/high/highest rules apply.
- When the hosted agent has quota again, it is fine to go back to it. Its model and effort come from your router, not from this wrapper.

