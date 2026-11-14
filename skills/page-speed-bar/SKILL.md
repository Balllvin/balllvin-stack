---
name: page-speed-bar
description: Use when shipping speed work on a web app, PWA, or desktop shell that has a hard per-page time budget (for example 800ms to first useful paint). Measure every main page, read backend logs for the same window, get a proposal before any code, then retest every page after merge.
---

# Page speed bar

Pick one number and hold every main page to it. 800ms to first useful paint is a good default. "Faster" without a number never finishes.

## Steps

1. List the main pages (home, the main list views, one detail page, settings). Load each one cold and time first useful paint against the bar. Record the numbers.
2. Read backend logs for the same time window. Look for duplicate requests, slow handlers (`elapsed_ms` or your equivalent), cache misses, and requests that block first paint but don't need to.
3. Hand one agent the measured issues and ask for a proposed fix only. Point it at your performance and simplification skills. No implementation yet.
4. Review the proposal. Push back where it guesses instead of measuring.
5. Tell the same agent to implement.
6. After merge and deploy, retest every page, not just the ones you changed. Done means every page is under the bar on the live site.

## Scope

A backend rewrite is in scope if that's the fastest honest path. Speed work is rarely frontend-only. Cut things before you add caches.

If you have a daily data job that a redeploy would interrupt, freeze merges around it and say the window in the repo docs.

## Don't

- Report a win from a local build or a warm cache.
- Chase one page while another regresses.
