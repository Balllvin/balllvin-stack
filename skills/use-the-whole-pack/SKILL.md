---
name: use-the-whole-pack
description: Use on any coding task in a repo that has a skill pack installed (pstack or similar). Apply every skill in the pack as far as it fits, including the heavy ones (arena, swarm, orchestrate, autopilot, hillclimb, statechart), name any skill you skip and why, and keep a short list of house rules that beat the pack's defaults.
---

# Use the whole pack

A skill pack only helps if the agent reads it. Agents tend to load two or three familiar skills and quietly skip the rest. This skill makes "use all of it" the default.

## Find the pack

1. Locate the installed skill files. Plugin caches usually live under a versioned path, so list the parent folder and read the version from its manifest (`plugin.json` or similar) rather than hard-coding a hash.
2. If the repo keeps its own copies (for example `.agents/skills/` or `.cursor/skills/`), read those too. Repo copies win when they disagree with the plugin.
3. Read the file every time. Don't work from memory of what a skill said last week.

## Default

Apply every skill in the pack as far as it can apply to the job. That includes:

- The top-level working-style skill and every playbook under it: investigation, bug fix, perf issue, hillclimb, runtime and trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot, session pickup, pause safely, multi-phase plan, worktree cleanup. End every code playbook with the opening-a-PR playbook.
- The heavy skills: arena, swarm, orchestrate, autopilot, and hillclimb. Use them when the job fits. Don't wait for someone to name them.
- The leaf skills whenever they touch the work: how, why, architect, tdd, interrogate, no-comments, blast-radius, language best practices, verification and formal-verification skills, statechart, benchmark checklist, technical writing, unslop, correct, reflect, teach, and every principle file.

If a skill can't apply, say which one and why. Never skip silently.

Use statechart together with a formal-verification skill for stateful product flows (sync, sharing permissions, job run states), where a small model can catch bad states before any code exists.

Run unslop on every PR description and commit message.

## House rules beat pack defaults

Keep a short numbered list of rules your team holds that override the pack. Write them in the repo (an `AGENTS.md` section or a rule file), not only in agent memory. Typical entries:

1. A hard product bar wins over any playbook. For example, if a playbook would add work that breaks a page-speed budget, the budget wins.
2. Pin the model and reasoning effort for cloud agents in one place, and don't let a setup skill change it.
3. Smallest change the evidence justifies. Simplification rules still apply.
4. Draft PRs only until a human says merge. Name any merge freeze windows (for example around a daily data job).
5. Anything paused stays paused until the owner un-pauses it.

## Encode process changes in the repo

When someone asks for a workflow change, put it in the repo as a draft PR (docs, skills, or rules). Memory alone gets lost between sessions and between agents.

## Don't

- Invent numbers in examples (prices, balances, metrics). Use clearly fake placeholders or real measured values.
- Run arbitrary model-written code on production hosts.
- Merge without an explicit go from the owner.

For a product repo, [references/product-repo-playbooks.md](references/product-repo-playbooks.md) maps common tasks to playbooks and lists the hard rules that ride along.
