# Design and scope

Start with the done-condition. The plugin is done when that sentence is true. Everything in the card has to serve it. Everything that serves a different sentence belongs in another plugin.

## How broad, how narrow

A plugin should be as wide as one job the model can finish without switching cards, and no wider.

Split when:

- The done-conditions differ. "The tests are green" and "the filing is in the workspace" are two conditions.
- The loop section of the card no longer fits on about one screen.
- Two people would reasonably enable one half and disable the other.
- One half must be locked (orders, money, connection edits) and the other must not.

Keep them together when:

- The actions always run in one loop toward the same done line.
- Splitting would force the model to stitch state by hand between two cards.
- The extra plugin would only expose one action that the first plugin already has to call every time.

A workbench that "does everything in domain X" is too broad: you cannot disable half of it, the card gets noisy, and ownership of tools blurs. A plugin per HTTP endpoint is too narrow: the model spends turns chaining trivia. The unit is the job, not the route.

Each action still follows one-job-per-action: do not hide multiple unrelated jobs behind one action's `mode` flag.

## Shared workspaces, separate plugins

Plugins may share a workspace (a project folder, a repo, a research workspace) without becoming one plugin. Name the workspace in each manifest's `state.location`. Do not reach into another plugin's private keys.

## Domain example (research and finance)

A researcher working an equity needs three jobs, not one mega-plugin:

| Plugin | Done when | Lives with |
|---|---|---|
| `equity.data` | Filings and prices for the ticker are in the workspace, or the fetch failed with a typed reason | Shared ticker workspace |
| `equity.valuation` | The model produced a valuation, or it failed a declared input check (missing statements, uncovered date) | Same workspace, reads what `equity.data` wrote |
| `equity.thesis` | The thesis was checked against the workspace facts, or the check stopped on a named gap | Same workspace, never places a trade |

Rules for sensitive domains:
- Keep draft/review plugins separate from execution. Never add irreversible money or order tools to research or analysis plugins.
- Lock execution/account plugins by default and require explicit server-side policy/approval gates.
- Short-lived scoped workspace tokens never read account credentials or money routes.

## Code tests, as a scope check

`code.tests` is one plugin because it has one done-condition: every test is green. Run, wake, edit the failing files with ordinary file tools, and rerun are one loop, not four plugins. There is no `fix` action. See [the worked example](code-plugin-example.md). If you later want a coverage budget or a performance gate, that is a second done-condition, so it is a second plugin that reads the same test artifact.
