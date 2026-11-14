---
name: ui-anti-slop
description: >-
  Use before building, reviewing, or restyling any web UI (Tailwind, CSS,
  React). Turns the design slop list into do/don't rules, a pre-ship checklist,
  and a self-verifying budget gate that enforces them. Pair with a repo's own UI
  skill when one exists.
---
# UI/UX anti-slop

Slop is decoration standing in for hierarchy. Fix it in this order: tokens and primitives, then lint and CI gates, and prose rules last. If a rule can be a token or a lint rule, make it one. Don't just write it down. If the repo has its own UI skill or taste doc, its tokens and rules win; this skill supplies the enforcement.

## Tokens first (Tailwind v4, example dark palette)

```css
@theme {
  --color-*: initial;            /* raw palettes (amber-500, sky-400) stop compiling */
  --color-bg: #0a0a0a; --color-fg: #e5e5e5; --color-muted: #a3a3a3;
  --color-surface: #111; --color-line: #222; --color-accent: #8fa6a3;
  --color-gain: #22c55e; --color-loss: #ef4444;
  --color-gain-tint: rgb(34 197 94 / .1); --color-loss-tint: rgb(239 68 68 / .1);
  --text-*: initial;             /* five sizes, far apart */
  --text-xs: 12px; --text-sm: 14px; --text-base: 16px; --text-lg: 20px; --text-xl: 28px;
  --tracking-*: initial; --tracking-normal: 0; --tracking-caps: .04em;
}
```
Use `bg-loss-tint`, not `bg-[var(--color-red)]/10`. Use `text-sm`, not `text-[11px]`.

## Rules

**Tags and pills.** Use a status word in its status colour, at most one per row.
- Do: `<span className="text-loss">Failed</span>`
- Don't: `<span className="rounded border px-2 py-1 text-[10px] uppercase tracking-[0.14em]">`, or two pills side by side.

**Italics.** Only for `em` inside rendered markdown or quotes. Never for emphasis, muted reasoning, or captions.
- Do: `text-muted`
- Don't: `italic text-muted`

**Type and tracking.** One UI face plus one mono for numbers and code. No Instrument Serif or other display serifs in product UI. No negative letter-spacing on headings and no tracked uppercase eyebrows.
- Do: `<h2 className="text-lg font-semibold">Holdings</h2>`
- Don't: `tracking-[-0.045em]`, or `text-[10px] uppercase tracking-[0.16em]` labels over headings.

**Detail.** A row shows a name plus at most two facts. Everything else goes on the detail page. Nothing below 12px.
- Don't: 9 to 11px meta lines, "N valid obs" pills, or a run ID next to a label.

**Dividers.** Group with space first, a rule second, a box last. Tables get one line under the header only.
- Do: `space-y-6`, or `thead { border-bottom: 1px solid var(--color-line) }`
- Don't: `border-b` on every row and `divide-y` inside bordered cards.

**Colour and opacity.** Neutral ink carries the screen. Colour is for data (gain, loss, status, series) and for one accent. Every tint is a token.
- Don't: `/10 /20 /30 /40` alpha ladders, `opacity-50` text, hex in components, or `text-red-400`.

**Containers.** A panel gets a border or a fill, never both, and never a panel inside a panel.
- Do: `<section className="bg-surface p-4">`
- Don't: `rounded border border-line bg-surface/70 p-4` wrapping more bordered boxes.

**Diagrams.** Draw a chart only when it shows real data. Prefer a sentence or a table to boxes and arrows. No decorative SVG.

**Code breadcrumbs.** Never render internal names: run or job IDs, file paths, `tool_name`, enum keys, stack traces. Show a date, a name, or a plain status.
- Don't: `<td className="font-mono">{run.run_id}</td>`

**Section numbering.** Headings are nouns. No `01 / 02`, no `${i + 1}. ${title}`. Steps get numbers only when the order is the content.

## Primitives over classNames

Ship `Text`, `Status`, `Panel` (fill only) and `Table` components. Screens compose those and never write raw size, tracking, alpha, or border classes. Lint every file outside `ui/` for those classes.

## Enforcement (local or pre-push gate; CI that never runs doesn't count)

Build the gate as one small script in the repo (for example a Node or Python file run on pre-push) that counts each slop pattern and fails when a count rises above its stored budget. Budgets start at the counts measured on main and only go down.

The gate has to prove it works before you trust it:
- Point it at the real UI source roots (for example `frontend/src`, `pwa/src`, `apps/*/src`), and fail if a root doesn't exist or no files match. A gate that scans an empty folder counts 0 and passes everything.
- Set one budget to 0 and check that it fails, then put the budget back.
- Hand-check a sample of matches for every pattern. Broad regexes (panels with border and fill together, step numbering, internal IDs in text) can over-count several times over, so tighten them until the samples are real hits.

Patterns to budget: font sizes below 12px (`text-[8-11px]`), uppercase plus tracking on the same element, ad-hoc alpha tints on token colours, raw Tailwind palette classes (`red-400` and the like), border plus rounded plus fill on one element, zero-padded or `index + 1` step counters, internal IDs rendered as text (`run_id`, `job_id`, `tool_name`, `request_id`), `italic` outside markdown, and negative letter-spacing. Font check: only the repo's allowed UI and mono faces get imported, and nothing matches `Instrument.?Serif`.

Avoid generic ESLint or stylelint "restricted class/value" configs that also scan the token file. They flag the token definitions themselves. If you add them, exclude the theme or tokens file and the UI primitives folder.

## Pre-ship checklist

- [ ] No `text-[9px]`, `[10px]` or `[11px]`
- [ ] No tracked uppercase eyebrows
- [ ] No panel with border, fill and rounded together
- [ ] No raw palette classes or ad-hoc `/10` tints when a tint token exists
- [ ] At most one status mark per row, and no stacked bordered pills
- [ ] No raw `run_id` or other internal IDs in mono
- [ ] No `01`/`02` step counters
- [ ] One line under table headers, not under every row
- [ ] The gate ran locally, failed when a budget was set to 0, and passed at the real budgets; say so in the PR
