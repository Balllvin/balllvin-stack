# Skill stack

Portable skills for AI agents: prompting, coding, reviewing, shipping, UI, writing, selling, and a few research and journaling routines. Each folder under `skills/` is one skill with a `SKILL.md` entry point and optional `references/` loaded on demand.

## Skills

### Coding and shipping

| Skill | What it does |
| --- | --- |
| [agent-prompt-engineering](skills/agent-prompt-engineering/SKILL.md) | Write and cut prompts, skills, and rules: direct language, one term per concept, a checkable done test, lean output contracts. |
| [orchestrate-subagents](skills/orchestrate-subagents/SKILL.md) | The parent keeps the task and primary files; children take bounded work with allowed files, forbidden files, and a done test. |
| [build](skills/build/SKILL.md) | How to build: delete, reuse, then write; fast-by-design rules, TDD, debugging, design principles, long-run working style. |
| [audit](skills/audit/SKILL.md) | Every review lens in one place: diff review, review waves, over-engineering, silent failures, performance, tests, types. |
| [security](skills/security/SKILL.md) | Scanners first, then threat model, discovery, validation, attack path, report, and fix, with agent and supply-chain threats. |
| [layered-spec](skills/layered-spec/SKILL.md) | A spec-only plan PR for multi-surface work: layered plan, parallel slices with zero file overlap, copy-paste implementer prompts. |
| [ship-verify](skills/ship-verify/SKILL.md) | From finished diff to merged, deployed, and verified: branches, PRs, CI, conflicts, review comments, smoke tests. |
| [use-the-whole-pack](skills/use-the-whole-pack/SKILL.md) | Apply every skill in an installed skill pack, name any you skip, and route product-repo tasks through the right playbook. |
| [coding-harness-router](skills/coding-harness-router/SKILL.md) | Start a coding run: a config-driven router picks harness and model, then the pack's matching playbook runs the work. |
| [cheap-local-coding-agent](skills/cheap-local-coding-agent/SKILL.md) | When cloud quota runs out, run a local CLI agent on a cheaper model: implement, second-agent review, effort per task, ordered fallbacks. |
| [wait-for-all-review-bots](skills/wait-for-all-review-bots/SKILL.md) | After triggering several review bots on a PR, wait for every one, then triage all feedback in one pass. |
| [post-merge-live-verify](skills/post-merge-live-verify/SKILL.md) | After a merge, wait for the deploy, open the live page, and check the change yourself before calling it done. |
| [page-speed-bar](skills/page-speed-bar/SKILL.md) | Hold every main page to one time budget: measure, read backend logs, propose before code, retest live after merge. |
| [fmp-integration](skills/fmp-integration/SKILL.md) | Use a metered market-data API without blowing the budget: one owner per data class, freshness classes, cost checks. |
| [bounty-workflow-authoring](skills/bounty-workflow-authoring/SKILL.md) | Keep exactly two standing bounty workflows (short and deep) and pick between them from difficulty signals. |
| [bounty-sizing](skills/bounty-sizing/SKILL.md) | Score a funded issue's difficulty and output one line: workflow, reasoning effort, reason. |
| [bounty-factory](skills/bounty-factory/SKILL.md) | Run a claimable bounty through fixed phases: problem, approach, implement, real-test, review, ship. |
| [shared-box-janitor](skills/shared-box-janitor/SKILL.md) | First-run setup for a cleanup agent on a computer shared by several agents: schedule, rules, baseline health check. |

### UI and sites

| Skill | What it does |
| --- | --- |
| [ui-ux](skills/ui-ux/SKILL.md) | Everything a person sees: data-first screens, honest states, motion, copy, landings, brand assets, rendered verification. |
| [ui-anti-slop](skills/ui-anti-slop/SKILL.md) | Concrete do/don't rules for web UI, design tokens, a pre-ship checklist, and a budget script that fails when slop counts rise. |
| [scroll-film-site](skills/scroll-film-site/SKILL.md) | Build a personal site that scrolls like a film: CSS scroll-driven scenes first, reduced-motion fallback, light motion budget. |

### Writing and posting

| Skill | What it does |
| --- | --- |
| [how-to-write](skills/how-to-write/SKILL.md) | Cut AI tells from any sentence (Unslop). |
| [how-to-write-paragraphs](skills/how-to-write-paragraphs/SKILL.md) | Make paragraphs and whole pieces move: one idea each, old then new, close on a consequence. |
| [post-topic-picking](skills/post-topic-picking/SKILL.md) | Decide whether something is worth posting: one concrete new fact, or "no post". |
| [post-structuring](skills/post-structuring/SKILL.md) | Chunk the material, condense each chunk to the data that matters, then simplify. |
| [voice-matched-drafting](skills/voice-matched-drafting/SKILL.md) | Draft in a person's own register from their corpus without copying post templates. Propose only, never post. |

### Selling

| Skill | What it does |
| --- | --- |
| [founder-led-first-customers](skills/founder-led-first-customers/SKILL.md) | Get the first ten customers by hand, by buyer type. |
| [founder-marketing-by-buyer](skills/founder-marketing-by-buyer/SKILL.md) | Pick how to sell from who the buyer is, with worked founder examples. |
| [historical-founder-selling](skills/historical-founder-selling/SKILL.md) | Selling lessons from industrial founders, with every claim tagged by source. |

### Research and journaling

| Skill | What it does |
| --- | --- |
| [research-notebook-ingest](skills/research-notebook-ingest/SKILL.md) | File a paper or article about models or hardware into the right research notebook with a short why-it-matters note. |
| [harvest-event-pages](skills/harvest-event-pages/SKILL.md) | Copy an event's about text and linked resources into a knowledge notebook without touching RSVP forms. |
| [trade-journal-why](skills/trade-journal-why/SKILL.md) | After a trade, capture the why, the why-not, and the timeframe as a timestamped journal entry. |
| [grill-portfolio-beliefs](skills/grill-portfolio-beliefs/SKILL.md) | Interview in rounds until hold and non-trade beliefs are explicit, and file the answers. |

Third-party sources and licenses: [skills/THIRD_PARTY_NOTICES.md](skills/THIRD_PARTY_NOTICES.md).

## Use

Copy a folder from `skills/` into your agent's skills directory (for example `.agents/skills/`, `.cursor/skills/`, or `~/.codex/skills/`). Skills cross-link by name or relative path like `../build/SKILL.md`, so copy the ones you use side by side.

## Credits

- **Poteto**, for Unslop and pstack.
- **[@balllvest](https://x.com/balllvest)**, who voice-noted a whole product strategy and then asked if it was already on GitHub.
