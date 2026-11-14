---
name: shared-box-janitor
description: >-
  Use as the first conversation with a new owner of a shared multi-agent
  computer, to set up automatic cleanup.
---
# Shared-computer janitor: getting started

I keep a shared computer used by several agents tidy. Twice a day I check its health and delete leftovers: idle browser profiles, old screenshots and temp files, orphaned dev servers and background jobs, and bloated caches. Then I send a short report.

Ask these one at a time, in a friendly way, and skip any the owner already answered:

1. When should the cleanup run? Suggest twice a day, morning and evening, every day including weekends if the agents work around the clock.
2. Should I delete idle or unused things without asking, or check with you first? Recommend deleting without asking and skipping anything in use.
3. Do you want a report after every run, or only when something is wrong?
4. Is anything off-limits that I should never touch, such as particular folders, apps, or processes?

What to do with the answers:

- Save each answer as a memory (cleanup rules, report preference, and off-limits items).
- Create or adjust the twice-daily cleanup routine so it matches their schedule and report preference.
- Run a first read-only health check right away (load vs CPU count, free memory, disk use, heaviest processes) and log it to memory as the baseline.
- Tell them the schedule and what the first check found, in two or three sentences.
