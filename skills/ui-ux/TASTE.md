# Taste for app screens

Use with `SKILL.md` and the app's UI architecture doc. That doc owns tokens and fonts. This file says how a working screen should look and read: dashboards, activity feeds, schedules, agents, memory, settings, tables, chat, and detail pages. Signed-out landings use `references/design.md` and `references/design/taste-skill.md`.

Adapted from `taste-skill` by Leonxlnx (v2.1.5 `references/app-screens.md`, `tells.md`, `copy.md`, `type.md`, `colour.md`, and v1/v2-experimental; MIT, Copyright (c) 2026 Leonxlnx) and `gemini-frontend-design` patterns (`google-gemini/demolab`, Apache-2.0), rewritten for working application surfaces.

## The test

Each screen answers one question first. Before building, say the question and the one finding the screen states ("Two automations failed today."). If the screen cannot name its question, it is two screens or none.

Then cut. Remove a word, a line, a box, or a section and look again. Keep the cut when nothing the person needs is gone. Placed space reads calm; leftover space reads unfinished.

## Hierarchy

- The page title is a noun at the app's title size. No hero band, no tagline, no subtitle that repeats the title ("Runs a task you saved").
- The data is the loudest thing on the page. A key number is large type with a small label, not a tile with an icon.
- One primary action per view. The most frequent job is one click away.
- Section headings are short and only exist when a page has more than one group. **No eyebrow labels over headings.**
- Headings are nouns. No `01` / `02` counters, Roman numerals, or `1.` prefixes unless order is the content, as in steps.
- Draw a diagram only for real data or a real flow. A sentence or a table beats boxes and arrows, and decorative SVG goes.

## Type

- One UI typeface plus the app's mono for code, identifiers, and compact columns. Never a third. Use `font-variant-numeric: tabular-nums` on the body face for prices, timers, and counts rather than adding a third monospace face.
- Four to six sizes, far enough apart to tell at a glance (for example 12, 14, 16, 24). If two sizes look almost the same, use one. Nothing below `12px`: no `text-[9px]`, `text-[10px]`, or `text-[11px]`.
- At most three weights. Differentiate subheadings, buttons, and labels with weight, family, and color instead of inventing intermediate font sizes. Secondary text is the same face in a softer ink, not lighter and smaller at once.
- Keep body paragraphs and body bullet or numbered lists at one consistent body scale. Never split consecutive paragraphs into an oversized lead paragraph above smaller paragraphs, or shrink body lists to caption size.
- Numbers that compare use tabular figures, right aligned, with fixed decimals in a column.
- Body measure stays near 45 to 75 characters. Do not centre paragraphs longer than three lines.
- Sentence case everywhere. No tiny tracked capitals as labels (`uppercase tracking-[0.14em]`).
- No negative letter-spacing on headings (`tracking-tight`, `tracking-[-0.02em]`). Reserve expressive display serifs for editorial landings, never working app screens.
- Italic only for `em` in rendered Markdown and quotes. Never for muted reasoning, captions, or missing values.

## Spacing and density

- One spacing scale, the app's own. Row pitch, padding, and type size move together: a denser table shrinks all three, never one.
- Group with space first, a divider second, a box last. **Never put both a border and a fill tone on the same panel:** `rounded border bg-[var(--color-bg-secondary)] p-4` is the failure. No panel inside a panel.
- Rows align on one left edge. Labels, values, and actions line up across rows.
- Pages use the full width the content needs. A narrow centred column on a wide screen reads unfinished.

## Colour

- Black, white, and neutral gray carry the screen. Colour goes on data: gain, loss, status, and chart series. Around `<= 3%` of a screen's pixels are coloured.
- One accent at most, for the main action or the current place, never both on every row.
- Every tint is a token. No alpha ladders (`bg-[var(--color-red)]/10`, `/20`, `/40`), no `bg-white/5`, no raw palette classes (`text-red-400`, `bg-zinc-900`), no hex in components. A missing tint goes to the design system / architecture doc as a token.
- A status is a plain word in its status colour, or a pale tint with dark text. No border, capitals, or tracking on it. One status mark per row; never two pills side by side. Reserve bordered or capsule shapes for interactive controls or genuine semantic status cells in data tables and API references; **never add decorative non-interactive chips or category tags of any shape inside cards or above headings.**
- No gradients, glass, glows, or shadows at rest. Overlays use the app's one overlay shadow.
- Text reaches WCAG AA 4.5:1 contrast. Muted text is still readable.

## Rows, lists, and detail

- Every row that has more to show opens it. Hover changes the row (wash or primary text) and the cursor, so the person can see it opens before clicking. Rows that do not open have no hover.
- Rows show the name and at most two facts the person scans for (status, last run). The rest lives on the detail page.
- Never render internal names: run or job IDs, request IDs, tool names, file paths, or enum keys. They are not facts the person scans for.
- A detail opens as its own page with its own URL and a back control. On phones the detail always pushes as its own view. Inline expanders are for one extra line, not for the item.
- The detail page shows everything: the inputs/prompt, tools, schedule, last result, history, and actions, with destructive actions last.
- Tables: grey sentence-case headers, no zebra stripes, one line under the header, not one under every row. A missing value is a gray `--`; a real zero prints `0`.
- Counts appear only on queues that need action. Never "Showing 80 of 10596" on a filtered view; count what is shown.

## States

- Loading uses the final geometry: skeleton rows the size of real rows. No shimmer, no centred spinner sentence.
- Empty keeps its frame and header plus one sentence that says what will appear here. Never empty copy that contradicts data elsewhere ("No facts yet" beside a populated list).
- Error sits in the block it belongs to, in one plain sentence (`Couldn't load <thing>` with Retry). Never a raw provider message, URL, status code, stack, or job name.
- Disabled controls look disabled and say why at the control when the reason is not obvious.
- Status words are one or two plain words: `Error`, `Running`, `Paused`, `Done`. Not "Did not run because..." in the row; the reason goes on the detail page.

## Motion

App motion is feedback only: press, hover, a menu or sheet opening, a value that changed. No entrance animations on pages, rows, or numbers. Values in `CRAFT.md`.

## Copy

- Use the product's own words for its objects. One name per thing across every screen.
- Buttons are one to three words that name the action: `Compact`, `Delete`, `Run now`.
- Short labels and status text have no trailing full stop. Full sentences keep theirs.
- No genre verbs (unlock, seamless, elevate, supercharge), no "Welcome back", no tricolons, no filler subtitles.
- A control explains itself. If it needs a paragraph, change the control.
- Removing tells without adding substance is also a tell. Every line that stays carries a fact or a choice.

## Tells to reject in review

Gradients or glass on app chrome; cards in cards; icons in tinted squares beside every heading; KPI tiles with icons; eyebrow labels; centred hero headers inside the app; emoji; monospace labels; more than two typefaces; three equal cards as a row; fake data (`99.99%`, `John Doe`); a colour on every row; two status marks on one row; a subtitle under every title; hover that does nothing; a row that looks clickable and is not; 9 to 11px text; alpha tints; bordered filled boxes; italic captions; numbered, Roman-numeral, or `[ 01 / 04 ]` section headings; clusters of separate bordered buttons for mode or filter choices; oversized lead paragraphs above shrunk bullet lists; decorative non-interactive badges or tags of any shape (capsule or square box); synthetic `LIVE` dots, `SCROLL` cues, or rotated edge text; run IDs on screen.

## Budgets

Enforce a monotonic slop budget in CI/local checks (for example `../ui-anti-slop/SKILL.md` and a budget script) that counts the failures above and fails when any count rises above its recorded baseline. After a cleanup, update the baseline down; never raise a budget to hide screen slop.

Fix slop where it starts: a size, tint, or status token in the design system, or one shared text, status, or panel component, then the screens. Do not hand-write sizes, tracking, alpha, or borders per screen.
