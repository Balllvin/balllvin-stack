# Third-party notices

Files under `skills/` that were copied or adapted from other projects. Paths are relative to `skills/`. Each row names the upstream and its license. "Adapted" means rewritten in our words from the upstream's ideas; "copied" means upstream text is kept (usually trimmed and edited). Licenses were checked against each upstream repository before publishing. Files whose upstream license could not be confirmed were left out of this repository.

## Apache License 2.0

Full license text: `ui-ux/references/design/hatch-pet/LICENSE.txt` (also at http://www.apache.org/licenses/LICENSE-2.0).

Attribution for every Apache-2.0 file below: the original work is Copyright its respective authors (OpenAI for openai/skills; Anthropic, PBC for anthropics/skills and anthropics/claude-plugins-official; Functional Software, Inc. d/b/a Sentry for getsentry/skills; Vercel, Inc. for vercel-labs/ui; Google LLC for google-gemini/demolab; NousResearch / unsupportedpastels for NousResearch/hermes-official-plugins), licensed under the Apache License, Version 2.0. These files were modified: trimmed, merged into hub skills, and edited to be project-neutral. Distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.

### openai/skills (https://github.com/openai/skills)

| File | Upstream |
| --- | --- |
| `ui-ux/references/writing/pdf.md` | `.curated/pdf` |
| `security/references/security-best-practices/**` | `.curated/security-best-practices` |
| `security/references/security-threat-model/**` | `.curated/security-threat-model` |
| `security/references/security-ownership-map/**` | `.curated/security-ownership-map` |
| `ship-verify/references/gh-address-comments.md`, `yeet.md` | `.curated/gh-address-comments`, `.curated/yeet` |
| `provider-routing/references/openai-docs.md` | `.system/openai-docs` |
| `ui-ux/references/design/imagegen/**` | `.system/imagegen` |
| `ui-ux/references/design/hatch-pet/**` | `hatch-pet` (ships `LICENSE.txt`) |
| `ui-ux/references/playwright/**`, `playwright-interactive.md`, `screenshot.md` | `.curated/playwright`, `playwright-interactive`, `screenshot` |

### anthropics/skills (https://github.com/anthropics/skills)

| File | Upstream | Basis |
| --- | --- | --- |
| `ui-ux/references/webapp-testing.md` | `skills/webapp-testing` | adapted |
| `ui-ux/references/design.md` (The five AI default looks) | `skills/frontend-design` | adapted |
| `ui-ux/references/writing.md` (Reader test) | `skills/doc-coauthoring` | adapted |
| `provider-routing/SKILL.md` (Live facts only) | `skills/claude-api` | adapted |

### anthropics/claude-plugins-official (https://github.com/anthropics/claude-plugins-official)

| File | Upstream | Basis |
| --- | --- | --- |
| `audit/references/code-review.md` | `plugins/code-review` | copied/trimmed |
| `audit/references/code-reviewer.md`, `pr-test-analyzer.md`, `silent-failure-hunter.md`, `type-design-analyzer.md` | `plugins/pr-review-toolkit` agents | copied/trimmed |
| `build/references/code-simplifier.md` | `plugins/code-simplifier` | copied/trimmed |
| `build/references/port-proof.md` | `plugins/code-modernization` | adapted |

### getsentry/skills (https://github.com/getsentry/skills)

| File | Upstream | Basis |
| --- | --- | --- |
| `ship-verify/SKILL.md` (When to stop iterating) | `skills/iterate-pr` | adapted |

### vercel-labs/ui (https://github.com/vercel-labs/ui)

| File | Upstream | Basis |
| --- | --- | --- |
| `ui-ux/BEHAVIORS.md` (behavioral kernel, layer stack, modality, boolean `data-*` state grammar, agent bridge, pattern/SSR/RTL testing) | `@ui-sdk/core` architecture and testing concepts | adapted |

### google-gemini/demolab (https://github.com/google-gemini/demolab)

| File | Upstream | Basis |
| --- | --- | --- |
| `ui-ux/SKILL.md`, `ui-ux/TASTE.md`, `ui-ux/references/design.md`, `ui-ux/references/design/landing-scene-variety.md` (opening format fit, non-split hero directions, 3-size body typography discipline, consistent prose/list scale, non-button selection controls, zero decorative chips, benefit-led whole headlines, scrolled visual audit) | `skills/gemini-frontend-design/SKILL.md` | adapted |

### NousResearch/hermes-official-plugins (https://github.com/NousResearch/hermes-official-plugins)

| File | Upstream | Basis |
| --- | --- | --- |
| `security/references/snapshot-evidence-and-closure.md` (commit `65f5ad93c7dc14dc661ff2ff3ead0fda71e7bd9d`) | `hermes-security` (`artifact-contract.md`, `worker-packet.md`, `core-scan.md`, `finding-details.md`, `validation-policy.md`) | adapted |

## MIT License

Each MIT upstream below is used under this notice, with the copyright line named in its section:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### cursor/plugins pstack (https://github.com/cursor/plugins/tree/main/pstack), Copyright (c) Lauren Tan

| File | Basis |
| --- | --- |
| `build/references/poteto-mode/**`, `build/references/principle-*.md` | copied (pstack 0.15.15) |
| `build/references/how/**`, `why/**`, `interrogate/**`, `architect/**`, `reflect/**`, `show-me-your-work/**`, `benchmark-checklist.md`, `correct.md`, and the other pstack skills under `build/references/` | copied |
| `orchestrate-subagents/references/arena.md`, `swarm.md` | copied |
| `build/SKILL.md`, `audit/SKILL.md`, `security/SKILL.md`, `provider-routing/SKILL.md` (evidence-or-label, measured number, explain-the-number) | adapted |
| `agent-prompt-engineering/SKILL.md` (A/B cut rule, `correct` ladder, schema-first cast) | adapted |
| `formal-verify/SKILL.md`, `audit/references/formal-verification.md` (`create-formal-verification-skill`, `statechart`) | adapted |
| `layered-spec/SKILL.md` (verifiable slice) | adapted |
| `ship-verify/SKILL.md` (briefing length) | adapted |
| `ui-ux/references/writing/unslop.md` | copied |

### cursor/plugins cursor-team-kit (https://github.com/cursor/plugins/tree/main/cursor-team-kit), Copyright (c) Cursor

| File | Basis |
| --- | --- |
| `ui-ux/references/control-ui.md`, `control-cli.md` | copied |
| `ship-verify/references/fix-merge-conflicts.md`, `get-pr-comments.md`, `new-branch-and-pr.md`, `review-and-ship.md`, `run-smoke-tests.md`, `weekly-review.md`, `what-did-i-get-done.md`, `ci.md` | copied or adapted |

### obra/superpowers (https://github.com/obra/superpowers), Copyright (c) 2025 Jesse Vincent

| File | Basis |
| --- | --- |
| `build/references/systematic-debugging.md`, `build/references/find-polluter.sh` | copied, in-file notice |
| `audit/references/receiving-code-review.md`, `requesting-code-review/**` | copied |
| `orchestrate-subagents/SKILL.md` (Review after every task, `subagent-driven-development`) | adapted |
| `agent-prompt-engineering/SKILL.md` (trigger-only descriptions, `writing-skills`) | adapted |
| `layered-spec/SKILL.md` (Global constraints, Review focus) | adapted |

### Leonxlnx/taste-skill (https://github.com/Leonxlnx/taste-skill), Copyright (c) 2026 Leonxlnx

| File | Basis |
| --- | --- |
| `ui-ux/references/design/taste-skill.md`, `gpt-taste.md`, `high-end-visual-design.md`, `industrial-brutalist-ui.md`, `stitch-design-taste.md`, `image-taste-*.md`, `imagegen-frontend-*.md`, `brandkit.md`; `ui-ux/references/redesign-existing-projects.md`; `build/references/full-output-enforcement.md` | copied |
| `ui-ux/TASTE.md` (v2.1.5 `app-screens.md`, `tells.md`, `copy.md`, `type.md`, `colour.md`, and v1/v2-experimental) | adapted |

### cloudflare/security-audit-skill (https://github.com/cloudflare/security-audit-skill), Copyright (c) 2025-2026 Cloudflare, Inc.

| File | Basis |
| --- | --- |
| `security/references/full-audit-confirmation.md`, `security/references/snapshot-evidence-and-closure.md` (commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`) | adapted |

### caldoai/skills (https://github.com/caldoai/skills), Copyright (c) caldoai

| File | Basis |
| --- | --- |
| `audit/references/untangle.md` (`skills/untangle-codebase/SKILL.md`) | adapted |

### Bil0000/Hill-Climb (https://github.com/Bil0000/Hill-Climb), Copyright (c) 2026 Bil0000

| File | Basis |
| --- | --- |
| `layered-spec/references/review-and-climb-layers.md` (Hill-climb slices), `build/references/poteto-mode/playbooks/hillclimb.md` (locked-check hill-climbing) | adapted |

### Other MIT

| File | Upstream | Basis |
| --- | --- | --- |
| `ui-ux/references/design/ui-ux-pro-max.md` | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | copied |
| `build/references/ponytail*.md` | https://github.com/DietrichGebert/ponytail | copied |
| `build/references/grilling.md` | https://github.com/mattpocock/skills | copied, in-file source line |
| `build/references/code-quality.md` (deep modules, deletion test, hot spots) | https://github.com/mattpocock/skills | adapted |
| `layered-spec/references/executor-plans.md` | https://github.com/shadcn/improve | adapted |
| `ui-ux/CRAFT.md` | https://www.skills.sh/jakubkrehel/skills/better-ui, https://github.com/emilkowalski/skills (Copyright (c) 2026 Jakub Krehel, Copyright (c) 2026 Emil Kowalski) | adapted |
| `audit/references/ui-polish.md` | https://github.com/emilkowalski/skills (7-viewport + touch + Slow 3G polish workflow) | adapted |
| `ui-ux/references/design/banner-design/**`, `design-kit/**`, `design-system/**`, `ui-ux/references/ui-styling/**` | ClaudeKit (`author: claudekit`, `license: MIT` in each file's frontmatter) | copied |
| `ui-ux/references/react-performance.md` | https://github.com/vercel-labs/agent-skills `react-best-practices` | adapted |

## Ideas only (rewritten, no text copied)

| File | Upstream |
| --- | --- |
| `audit/references/differential-review.md` | https://github.com/trailofbits/skills `differential-review`, `variant-analysis` (CC-BY-SA-4.0) |
| `security/references/insecure-defaults.md` | https://github.com/trailofbits/skills (CC-BY-SA-4.0) |
| `fmp-integration/SKILL.md` ("Unavailable is not clean") | https://github.com/trailofbits/skills `supply-chain-risk-auditor` (CC-BY-SA-4.0) |
| `security/references/hunt-loop.md` | Capital One VulnHunter, https://github.com/nealbridges/VulnHunter (Apache-2.0) |

## Quoted examples and writing rules

| File | Upstream |
| --- | --- |
| `ui-ux/references/writing/unslop.md` (rules 28, 29, 34) | https://x.com/hugo_edwards_/status/2120380614365028391 (in reply to https://x.com/zhizdev/status/2119874095269707977) |
