# Delegation

Every non-trivial task loads `orchestrate-subagents` and uses sub-agents effectively without being asked: explorers for mapping, parallel workers for independent helper slices, critics and verifiers for review. The parent keeps the primary path, git, and the PR. Write each child prompt with `../agent-prompt-engineering/SKILL.md`. Omit task `model` so children inherit the parent model unless the user specifies a model and effort.

Follow `orchestrate-subagents`. The parent implements and orchestrates. Sub-agents do bounded parts: exploration, isolated slices, review, repair, validation. Do not hand them the whole task, the PR, or git. Name primary files first, keep them out of worker allowed files, and edit at least one yourself before treating worker diffs as done. Two agents must not mutate the same file, lockfile, or checkout. Skip workers for tiny edits.

A non-trivial task that finishes with no sub-agent misses the second read and context isolation. Spawn bounded helpers where they add completeness or speed, while keeping primary edits and git/PR ownership with the parent.
