# Plans for a cheaper executor

A slice is executed by an agent that did not see the spec thread and may run on a smaller or cheaper default model. Write every slice so that agent can finish it from the plan alone. The plan is the product. Adapted from [shadcn/improve](https://github.com/shadcn/improve) (MIT).

Load this when writing or reviewing Layer 6, the slice-agent template, or any plan meant for another agent.

## Rules

1. **Self-contained.** Put the context the executor needs in the slice: why the change matters, exact paths, a current-state excerpt, the convention to match (with an exemplar path already in the tree), and each step's verification command with its expected output. A slice that says "as discussed above" or "see the earlier section" is broken.
2. **Excerpts from your own reads.** Open every cited file yourself before you quote it. A subagent's line number is a lead, not a fact. Wrong excerpts fail the drift check below.
3. **Written against a commit.** Stamp each slice (or the spec once, if every excerpt is from the same tree) with `git rev-parse --short HEAD`. The executor's first step is to confirm those paths still match. If they don't, that step stops; the executor reports `Found:` and does the rest of the slice that is still valid.
4. **STOP if.** Each slice names the conditions that halt a step: the excerpt drifted, a named file is gone, a forbidden path is required, or a stated assumption is false. "Stop" needs that scope so the executor does not quit the whole slice. See `../../agent-prompt-engineering/SKILL.md`.

Owns, Forbidden, Depends, and Done-when already live on the slice template in the skill. Use them. Do not restate them here.
