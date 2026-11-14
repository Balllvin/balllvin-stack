---
name: post-merge-live-verify
description: Use right after a product PR merges, to confirm the change on the live site after the deploy finishes. Tests, a green CI run, and screenshots of local HTML don't count as the live check.
---

# Post-merge live verify

A merged PR isn't a shipped change until someone has looked at it on the live site.

## Do

1. Note the merge commit, the user-facing URL, and which service should pick it up.
2. Schedule a one-time check about 10 minutes after the merge (whatever your deploy usually takes). Don't skip it because CI was green.
3. When it runs, confirm the merge commit is actually serving: the deploy for the right service shows success and active. Then open the live URL in a real browser, use the changed UI, and take a screenshot.
4. Report only what the live page showed. If the deploy is still building, say so and schedule another short check. If the UI is still wrong, fix it.
5. Remove the scheduled check once it has reported.

## Don't

- Claim a UI change is live from a merge time or a unit test.
- Ask the user to retest before you've looked at the live page yourself.
