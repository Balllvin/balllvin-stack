---
name: wait-for-all-review-bots
description: Use after you trigger automated reviewers on a PR (a comment command or label that starts several review bots), before you call the review round done or start acting on the feedback.
---

# Wait for all review bots

One trigger often starts several bot reviewers. The round isn't done until every one of them has left feedback. Acting on the first reply means you miss the rest, or redo work when the later ones land.

## Check

1. Know how many bots the trigger starts.
2. Note the time of your trigger comment.
3. List reviews and review comments after that time, for example `gh api repos/OWNER/REPO/pulls/N/reviews` and `.../pulls/N/comments`.
4. Tell the bots apart by a stable id in each review (an automation id in the body or header, or the bot account).
5. Go on only when the count of distinct bots for this round matches the expected number. Inline threads from some of them mean not ready yet.

## Then

Hand all the feedback to one agent. It sorts each item into correct, wrong, or out of scope, implements only the correct ones, and replies on the rest with a short reason.
