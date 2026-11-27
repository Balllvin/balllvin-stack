---
name: ui-ux
description: Use for product screens, navigation, settings, motion, UI states, copy, messages and notifications, landings, visual assets, documents, and rendered UI verification. Dense data apps (tables, finance, research) especially.
---

# UI and UX

Make the app a clear, comfortable tool for research and decisions. Lead with the user's evidence or task. Give chrome less attention.

## Authority and context

- Follow `AGENTS.md` for workflow, contracts, validation, and file-size gates.
- Read the app's UI architecture doc, if any, for tokens, navigation, and platform behavior.
- Read `TASTE.md` for how a working screen looks and reads, `CRAFT.md` for interaction values, and `BEHAVIORS.md` for SSR-first islands, the headless kernel, overlay layer stack, keyboard/focus rules, boolean `data-*` attributes, and agent readiness. App architecture docs own explicit platform exceptions.
- Read `references/writing.md` for prose and `references/design.md` for landings, brand, and media.
- Explicit user direction wins over style defaults. Filters prevent careless defaults; they do not prescribe a terminal aesthetic.
- Keep app-specific rules in the architecture doc. Record concrete user feedback there, newest first.

## Architecture and shared UI primitives

- **SSR-first with small interactive islands.** Render pages complete on the server so core reading, navigation, and form submissions work with JavaScript off. Add client interactivity only as small `data-island` roots mounted by one shared headless kernel (`BEHAVIORS.md`).
- **One owner per primitive.** Reuse shared page shells, formatters, icon sets, and error helpers across screens.
- **Zero-dependency ratchet.** Never add a runtime UI or animation library when the headless kernel or CSS handles it (`BEHAVIORS.md`).

## 6-step UI/UX SOP

Before writing or restyling a screen, run these six steps in order:

1. **Classify job and screen archetype:** Name the user decision and pick the archetype (`ops_console`, `split_workbench`, `focused_form`, `landing_showcase`, `genui_inline`, or `threejs_viewport`; see `TASTE.md`).
2. **Lock user truth and states:** Trace real facts, requested workbench controls, loading skeletons, empty copy, `Couldn't load <thing>` + Retry errors, `data-agent-confirm` on destructive actions, and `data-agent-secret` on secrets.
3. **Choose archetype geometry and focal hierarchy:** Use wide fluid canvases (`>= 1200px`) for `ops_console`, hairline-split 2-pane layouts for `split_workbench`, focused `560-680px` measures for `focused_form`, full-bleed live proof for `landing_showcase`, or `>= 70%` canvas for `threejs_viewport`. Reject both bloated AI-SaaS box-soup and sterile 1998 wireframe emptiness.
4. **Set typography, alignment, and semantic color (`<= 3%`):** Separate scale cleanly, right-align `tabular-nums` for comparable numbers, reserve mono strictly for code/IDs/SQL/hashes, keep contrast `>= 4.5:1`, and reserve semantic color for critical status and primary actions.
5. **Apply Motion Decision Matrix:** Keep `ops_console`, `genui_inline`, and data switches at `0ms`; limit micro-feedback to `100-160ms`; reserve `180-240ms` spatial transitions for transient drawers/modals and `250-450ms` expressive transitions for `landing_showcase`; ban `transition: all` and infinite working-surface loops; always ship `@media (prefers-reduced-motion: reduce)`.
6. **Cut and verify:** Inspect `1440x900` and `390x844` (`>= 44px` tap targets), keyboard/focus recovery, honest error/empty states, zero slop tells, and zero sterile dead space.

## Start with the page's job

Before editing, name the app, the object, the user's next decision, and the evidence needed for that decision.

Example: "Portfolio. Show holdings and today's change so the person can choose what to inspect."

1. Inventory every reachable route, tab, sheet, menu, and settings panel in scope.
2. Trace the real data and actions before changing their presentation.
3. Inspect loading, populated, empty, failed, stale, partial, and unauthorized states.
4. Find the shared owner before fixing the same defect on several pages.
5. Render the current screen. Diagnose it before adding styling.

For a large browse table (a watchlist, inbox, or catalog):
1. Make list selection, view selection, filtering, and the virtualized table the initial screen. Mount research or ranking work when the person opens that workflow.
2. Compare paint rows with the selected list's total from that same response. Keep a partial preview visible while one scoped read loads the complete table, and expose loading or failure beside it.
3. Keep the table in a `flex min-h-0 min-w-0` chain to the viewport. Give columns minimum readable widths and flex growth so short presets fill wide screens while narrow screens scroll inside the grid.
4. Check a list of several hundred rows, a 30-row preview, a list whose count grows or shrinks during switching, a pending switch, and a failed refresh. Assert complete settled row identity, zero automatic research/ranking requests, and preservation of only the selected list's last-good rows. Inspect grid bounds and keyboard sorting at `1440x900` and `390x844`.

## Data first

- Put the useful value, document, result, conversation, or next action in the first viewport.
- Keep page titles small and subordinate. Omit a visible title when navigation, columns, or the object already identify the content.
- Keep accessible names and document structure when deleting visible headings.
- Name units, periods, currency, provenance, and freshness where they change interpretation.
- Use `font-variant-numeric: tabular-nums` on the body face for comparable numbers. Reserve monospace for code, identifiers, and compact numeric columns. Never add a third typeface just for numbers.
- Use readable sans-serif text for names, explanations, settings, navigation, and actions.
- Keep missing values as `--`. Never substitute zero, sample data, or a neutral verdict for unavailable evidence. Hide a metric group when every value in it is missing.
- Say each label once per row. Never print a raw enum and its humanized copy together, or repeat one label down many rows; group identical rows with a count.
- Separate what the user owns from ideas and watchlists, and name each section in plain words.
- Apply gain/loss color to the displayed rounded value. A displayed zero is neutral.
- Put controls beside the data they change. A detail pane adds evidence the adjacent table does not already show.
- Keep dense tables useful on desktop. On phones, prioritize essential columns and contain horizontal scrolling inside the table.

## App comfort and visual craft

High taste avoids both failure poles (`TASTE.md`): over-decorated AI-SaaS box-soup (eyebrows, card-in-card, pill walls, purple neon/glass, fake `Acme`/`99.99%` data) and under-crafted 1998 wireframe sterility (raw tables marooned in dead empty space, flat hierarchy with unemphasized `SEV-1` rows, ragged left-aligned numbers, missing workbench controls). Match layout and density to the screen archetype (`ops_console`, `split_workbench`, `focused_form`, `landing_showcase`, `genui_inline`, `threejs_viewport`):

- Reuse each app's tokens, typography, controls, skeletons, and formatters.
- Build hierarchy with spacing, readable type, alignment, and selective emphasis.
- Keep one canvas. Use dividers only where they clarify groups, rows, or pane boundaries.
- Fewer layers, never ambiguous controls. Removing plates and lines must not remove affordance: every button keeps a border or fill, a hover state, and a focus state, so it never reads as plain text. Contextual hover-revealed icon actions stay bare icons with a hover wash.
- Never put both a border and a fill tone on the same panel (`TASTE.md`). Flatten nested cards and panels, and give in-flow content no elevation or shadow.
- Start sections directly with their heading. Never place eyebrow labels or decorative non-interactive badges, chips, or category tags (capsule or bordered box) above headings, over images, or inside cards; reserve bordered or capsule shapes for interactive controls or genuine semantic status cells.
- Prefer black, white, and neutral gray. Primary data such as identifiers and names uses the normal text color, never an accent or off-gray tint.
- Use quiet rounded controls and native grouping where they improve recognition and touch comfort.
- Keep numeric grids precise. Do not make every screen a square terminal or a grid of decorative cards.
- Use cards for separate objects or contained interactions. Avoid cards inside cards and duplicate surrounding plates.
- Keep radii consistent by role. Nested visible corners follow outer radius = inner radius + inset.
- Use the app's existing overlay fill and shadow to distinguish menus and sheets from content, sitting in the top layer so no scroll container clips them.
- Express open, checked, selected, highlighted, pending, disabled, invalid, and motion states through the boolean `data-*` and `data-slot` attributes defined in `BEHAVIORS.md` (never `data-state`). Preserve author `id` / `aria-*` attributes.
- Keep semantic color meaningful. Do not introduce a new palette, font, or component library for polish alone.
- Never dim a filled accent control with opacity to show disabled. Prefer `aria-disabled="true"` for focusable async/disabled actions, or switch to a bordered neutral control.
- Keep body and secondary text at WCAG AA contrast. Small text needs more care than large values.
- Show hover, pressed, selected, disabled, and keyboard focus as distinct states. Gate virtual list/menu highlights on `data-modality="keyboard"` so pointer movement does not fight arrow keys.
- Gate hover effects to `hover: hover` and `pointer: fine`. Touch must not depend on hover.
- Use at least 44px touch targets and 16px phone text inputs. Respect zoom, safe areas, and the software keyboard.
- Preserve user text selection. Apply `touch-action: manipulation` to tap controls, not gesture canvases or scroll containers.

## Flows and settings

- Show the common path first. Put advanced inspection one level deeper.
- One object per page. Switch objects from one compact header dropdown, never a stacked list of every object as page chrome.
- Split a crowded page into a few plainly named views with an obvious switcher instead of one long scroll.
- Use non-button selection controls for mode, size, filter, or setting choices: connected segmented controls, tabs, radios, switches, `<select>`, or direct manipulation, never clusters of separate bordered buttons.
- Never put an always-visible text input beside every row. Use an explicit button such as "Add note" that reveals the input.
- Use one primary action per task. Remove duplicate controls and unnecessary steps. Gather secondary actions into a compact menu (`Add`, `…`) rather than stacking bordered buttons down the page.
- Autosave ordinary edits quietly. Keep drafts after failure and preserve both versions on conflict.
- Scope busy and failed state to the item it belongs to. One row's request or one bad item must not freeze or fail the whole list or panel.
- Keep a confirmed snapshot for optimistic updates. Roll back or reconcile failed writes visibly.
- Confirm destructive or irreversible actions (and mark with `data-agent-confirm`). Give reversible actions direct manipulation or keyboard/pointer reorder plus undo. Mark token/secret controls with `data-agent-secret` so agent snapshots redact them.
- Keep settings names, groups, defaults, and persisted meaning aligned across clients using the same account.
- Explain device-only settings at the relevant control. Do not offer inert substitutes for keychain, updates, or folder access.
- Keep deep links, selected navigation, tabs, and route state consistent.
- Give icon controls accessible names. Keep primary and recovery actions reachable by keyboard and touch with single-tab-stop roving focus on composite widgets.
- Menus, dialogs, sheets, selects, and popovers use the shared overlay layer stack (`BEHAVIORS.md`) on web and the system menu on native.
- Check Esc dismissal precedence, modal `inertOutside`, scroll lock, focus return (`finalFocus` -> trigger), viewport edges, and submenu travel.

## Honest state and perceived speed

- Skeleton only the first blocking load. Match the geometry of the loaded content.
- Keep populated content visible during refresh. Mark the affected region busy and show a short refresh status.
- Show empty copy only after a successful settled read.
- Put failure and Retry beside the affected content. Never describe failure as absence.
- Word read failures plainly as `Couldn't load <thing>` with Retry. Never add a reason that implies deleted data ("It no longer exists") or repeat the button's words ("Try again" beside Retry).
- Show routine cache age quietly. A timestamp is not a failed request. Reserve warning and Retry for a completed failure; keep partial-data facts local and unresolved write errors visible.
- Clear the previous read error when a new attempt starts. Show a new failure only after that attempt settles. A successful read must not dismiss a save, conflict, import, or action error.
- Clear busy state after failed streams. Preserve the prompt and saved trail.
- Hold private chrome behind a confirmed session. Unavailable auth shows recovery; confirmed sign-out goes to login.
- First paint uses bounded reads. Defer hidden tabs and expensive secondary requests.
- Check unbounded lists, request waterfalls, oversized payloads, and unstable live renders on hot routes.
- Keep chart geometry stable across loading, failure, and range changes.
- Do not swallow errors or announce success before a write is confirmed.

For screen switches, hidden panels, live progress or imports, read [reuse and work budgets](../build/references/reuse-and-budgets.md). Verify first paint, focus, interval, unmount, next-hop reuse and ten rapid switches. CSS hiding does not stop effects; a healthy stream must gate equivalent fallback polling without weakening recovery.

## Motion with a purpose

Use motion only for feedback or spatial context, following the `TASTE.md` Motion Decision Matrix:

- **Without animation (`0ms`):** `ops_console`, `genui_inline`, data tables, live numbers, and `split_workbench` data switches update immediately with zero entrance staggers or infinite decorative loops.
- **Micro-feedback (`100-160ms`):** Hover wash (`@media (hover: hover) and (pointer: fine)`) and subtle `scale(0.98)` press; keyboard shortcuts and data commits never wait for motion.
- **Spatial transitions (`180-240ms`):** `cubic-bezier(0.22, 1, 0.36, 1)` on `opacity` + `transform` ONLY for transient drawers, menus, sheets, and `focused_form` modals.
- **Purposeful expressive (`250-450ms`):** Allowed on `landing_showcase` hero/demo transitions; compositor-only (`transform`, `opacity`, `clip-path`), non-blocking, never stuck at `opacity: 0`.
- **Mandatory hygiene:** Never use `transition: all`; always pair any CSS transition or `@keyframes` with `@media (prefers-reduced-motion: reduce)` at equal specificity; never add pointer-tracking, scroll hijacking, or new animation libraries (`CRAFT.md`, `BEHAVIORS.md`).

## Web and native parity, chat surfaces

- Match web and native capabilities, labels, persisted settings, state handling, and recovery for shared jobs.
- Adapt layout and controls to the platform. Folder access, keychain, and auto-update remain device capabilities.
- Keep one floating oval composer. Context chips share its overlay without a surrounding footer plate or divider.
- Show the reply directly. Keep traces and sources in message overflow; keep artifacts and run cards in the reply.
- Traces open a viewport-contained overlay on web and native inspection in native apps. Show full reasoning, named tools, and child receipts.
- Render stored content as readable documents, including tables, lists, quotes, code, and links.
- Stream partial replies as plain text. Never parse partial text as Markdown; the saved message replaces it.
- Preserve source content and drafts when changing presentation. Failed, processing, empty, and stale sources remain distinct.
- Test one source of each supported kind, including failed imports and long table content.

## Precise words

- Read `references/writing/unslop.md`. Keep its rules intact.
- Use sentence case and short concrete verbs. Explain the failure and the next useful action.
- Delete repeated titles, route descriptions, marketing claims, and internal implementation jargon.
- Do not remove necessary units, permission consequences, financial risk, or recovery instructions to shorten copy.
- Use no decorative emojis, em dashes, or en dashes in new product copy. Preserve user-supplied text verbatim.
- Keep headlines whole without `<br><em>` italic splits, and cut fourth-wall commentary about the interface itself.
- Fix poor AI-written content in its producing prompt. Lead with the answer and cite evidence inline.

## Signed-out pages

Landings follow `references/design.md` and `references/design/taste-skill.md`: one job per page, one call to action (never pair every primary button with a ghost or underlined link by default), live data or product proof as the hero, no pill walls, no section eyebrows, no bottom KPI or spec strip on the hero, and far fewer words than feels safe. Non-hero public formats (docs, directories, utilities, blogs) open directly into live content instead of a full-screen marketing banner. Hero-led pages skip the 50/50 split template and let the headline and lead visual command the full width, center, or depth of the viewport, bleeding to `y = 0` behind a borderless header that gains clean surface separation on scroll. Keep hero supporting copy to at most 25 words and lead marketing headings with user benefits rather than raw specs. Public copy and account actions render without JavaScript or motion.

## Verify and critique

1. Run the app and inspect the rendered change before calling it done (run any repo slop-budget, golden-HTML, and dependency-ratchet gates).
2. Check responsive web changes at `390x844` and `1440x900`; use supported window sizes for Native. Capture both the opening viewport and scrolled below-the-fold sections at desktop height plus mobile, and inspect the rendered screenshots directly for single-line desktop nav, scrolled header separation, zero text or visual collisions, consistent type hierarchy to the footer, and zero overflow or clipped display words. Include states affected by the change.
3. Stress with long names, long URLs, large counts, missing values, narrow screens, zoom, and awkward tables.
4. Drive real keyboard and touch paths. Load changed SSR pages with JavaScript off and confirm they read and submit. Check WAI-ARIA pattern compliance (`checkPattern`), kernel SSR safety (`checkServer`), RTL direction (`checkDirection`), agent discovery/redaction (`snapshot()` / `act()`), focus recovery, names, contrast, dialogs, scrolling, and reduced motion.
5. Reproduce bugs before fixing them. Keep behavior tests that fail when the fix is reverted.
6. Render Native views offscreen with test data. Do not inspect the owner's running app or credentials.
7. For a changed shared job or setting, check its web and native contracts. Record intentional platform differences explicitly.
8. Iterate with focused checks, then run the affected final gate required by `AGENTS.md`.
9. Give a fresh critic the integrated diff. The parent reviews every finding and owns the final decision.
10. Record route coverage, screenshot paths, commands, failures, and unavailable checks. A source audit does not prove a rendered screen.

Report polish findings as `Severity | Location | Before | After | Why`. Block on broken interactions, misleading data, inaccessible recovery, or lost drafts.

## References

Files over 600 lines are catalogs: search them for the section you need.

| Reference | Read when |
| --- | --- |
| `TASTE.md` | Any working app screen: hierarchy, type, spacing, colour, rows and detail pages, states, copy, tells to reject, and slop budgets. |
| `BEHAVIORS.md` | SSR islands, the headless kernel, overlay layer stack, roving focus, modality, boolean `data-*` attributes, agent readiness, and pattern/SSR/RTL verification. |
| `CRAFT.md` | Reviewing nested surfaces, icons, press/hover, or motion values. |
| `MESSAGES.md` | Writing messages or question cards to the person. |
| `references/writing.md` | Any prose: full Unslop, technical writing, reader test, PR bodies, document formats. |
| `references/writing/unslop.md` | The source Unslop catalog. |
| `references/writing/technical-writing.md` | Docs, RFCs, READMEs: Diataxis modes, style, review checklist. |
| `references/writing/pdf.md` | Creating, editing, and rendering PDFs. |
| `references/design.md` | Any landing, brand, image, or video work; routes to everything under `references/design/`. |
| `references/design/taste-skill.md` | Landing, portfolio, or redesign taste: dials, AI tells, pre-flight. |
| `references/design/landing-scene-variety.md` | Any multi-scene landing or scroll film. |
| `references/design/high-end-visual-design.md`, `gpt-taste.md`, `industrial-brutalist-ui.md`, `stitch-design-taste.md`, `ui-ux-pro-max.md` | Style catalogs for a specific landing brief (restrained, premium, GSAP editorial, brutalist, Stitch `DESIGN.md`, palette and font catalog). |
| `references/design/image-taste-frontend.md`, `image-taste-art-direction.md`, `imagegen-frontend-web.md`, `imagegen-frontend-mobile.md` | Image-first comps before building web or mobile screens. |
| `references/design/imagegen/index.md` | Generating or editing images. Extras in `references/`: `cli`, `image-api`, `prompting`, `sample-prompts`, `codex-network`. |
| `references/design/brandkit.md` | Brand boards and logo systems as images. |
| `references/design/banner-design/index.md` | Banners. Extra: `references/design/banner-design/references/banner-sizes-and-styles.md`. |
| `references/design/design-kit/index.md` | Logos, CIP, icons, social photos, HTML slides. Extras in `references/`: `design-routing`, `logo-design`, `logo-style-guide`, `logo-color-psychology`, `logo-prompt-engineering`, `cip-design`, `cip-style-guide`, `cip-deliverable-guide`, `cip-prompt-engineering`, `icon-design`, `social-photos-design`, `banner-sizes-and-styles`, `slides`, `slides-create`, `slides-strategies`, `slides-layout-patterns`, `slides-copywriting-formulas`, `slides-html-template`. |
| `references/design/design-system/index.md` | Brand token architecture. Extras in `references/`: `token-architecture`, `primitive-tokens`, `semantic-tokens`, `component-tokens`, `component-specs`, `states-and-variants`, `tailwind-integration`. |
| `references/design/hatch-pet/index.md` | Animated Codex pets. Extras in `references/`: `animation-rows`, `codex-pet-contract`, `qa-rubric`, `scripts/`, `LICENSE.txt`. |
| `references/playwright/index.md` | Driving a real browser. Extras in `references/`: `cli`, `workflows`. |
| `references/playwright-interactive.md` | Iterative UI debugging with a persistent browser or Electron session. |
| `references/webapp-testing.md` | Starting servers before a Playwright run and picking selectors. |
| `references/react-performance.md` | Hot routes, shared clients, lists that re-render on live data. |
| `references/screenshot.md` | The user asks for a desktop, window, or region screenshot. |
| `references/control-ui.md`, `control-cli.md` | Local harnesses for web/Electron UI or CLI/TUI checks. |
| `references/ui-styling/index.md` | shadcn/ui and Tailwind. Extras in `references/`: `shadcn-components`, `shadcn-theming`, `shadcn-accessibility`, `tailwind-utilities`, `tailwind-responsive`, `tailwind-customization`, `canvas-design-system`. App tokens win. |
| `references/redesign-existing-projects.md` | Auditing an existing surface before a redesign; use its audit, not its premium styling. |
