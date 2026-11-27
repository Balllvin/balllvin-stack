# Design

Expressive visuals: pages that sell, and assets that carry a brand. The old taste, landing, brand, image, and video skills now live under `design/`, a reference of the `ui-ux` skill. This file routes to them and holds the rules that apply across all of them.

## Which rules

| Surface | Rules | Why |
| --- | --- | --- |
| Signed-out landing, marketing route, welcome page, portfolio site, brand asset, image, video, game | this file | The job is persuasion or identity. Taste and variety matter. |
| Anything behind a login: data views, tables, settings, chat, admin, workspaces | `../SKILL.md` + `../TASTE.md` | The data is the product. Taste machinery (glass, marquee, hover-scale, big type) slows decisions and hides failures. |
| Signed-out page that shows the product | both | This file owns layout and motion; the product rules' honesty, tokens, and failure states still apply. |

The app UI architecture doc wins for its app. `AGENTS.md` wins on workflow, file-size gates, and data-provider routing. Inside this reference, this file's anti-slop, typography, and hero rules override conflicting defaults in upstream catalogs (such as 50/50 split heroes or section eyebrows in `taste-skill`), and `taste-skill` owns the dials and brief-to-system map.

## Design read first

Before editing, write one line: surface, audience, the one decision the page asks for, and the proof. Example: "Reading this as: signed-out research-app landing; promise is research you can cite; decision is create account or leave; proof is an animated product mock." This stops the model reaching for the aesthetic it used last time.

When the aesthetic is open, derive palette, contrast, and layout rhythm from the subject's real materials, environment, and audience rather than generic category reflexes. Then pick dials (`taste-skill` section 1): design variance, motion intensity, visual density. Say them. A brief for a bank and a brief for a game studio should not land on the same numbers.

Match the opening screen to the format. News front pages, blogs, documentation, dashboards, search or directory indexes, utility tools, and resumes open directly into live content, a masthead and story grid, a workspace, or a document sheet. Never push articles, controls, or data below a `100dvh` marketing banner.

## Composition, navigation, and typography

- **Single-line nav and hero bleed.** Keep desktop navigation on one compact line, with the brand title, masthead, or wordmark noticeably larger or bolder than menu links. On hero-led pages, let the hero surface, image, or gradient bleed to `y = 0` behind a borderless header bar; if the header stays fixed on scroll, give it clean surface separation once scrolled so content never collides behind nav links.
- **Color beyond beige and dark neon.** Unless the brief asks for warm beige with terracotta or dark slate with neon purple, explore a wider spectrum grounded in the subject: chromatic color-blocking, deep roast/forest/ink/marine darks, cool architectural stone or silver, sunlit pastels, or crisp gallery light. Define theme tokens for page background, subtle secondary surface, primary text, muted text (4.5:1 WCAG AA), and one accent.
- **3-size body typography discipline.** Use at most 2 font families: one versatile sans across weights, or a purposeful 2-font pairing. Do not default every creative brief to a display serif plus generic sans; geometric, neo-grotesk, or expressive sans display faces are often stronger. Never add a 3rd monospace font for prices, timers, or counts when `font-variant-numeric: tabular-nums` on the body face works (reserve mono for code, docs, or terminal tools). Lock at most 3 distinct body font sizes below the fold (`heading`, `body`, `sm`), differentiating `<h3>`, buttons, and labels with weight, family, and color instead of inventing intermediate `20px` to `24px` steps (allow a 4th compact step only on an explicitly requested dense dashboard or table). Hero `<h1>` and the navbar brand wordmark are exempt from the 3-size limit, while no text above the fold drops below `13px` (`0.8125rem`). Keep all body paragraphs and bullet or numbered lists at one consistent body scale (no oversized `.lead` paragraph above smaller paragraphs, no caption-sized body lists). Keep body prose `<= 65ch`, use sentence case for UI labels, and tighten display tracking (`-0.02em` to `-0.05em`) on landing display type only (app screens forbid negative tracking per `../TASTE.md`).
- **Abandon the 50/50 split hero template.** On hero-led pages, do not trap `<h1>` in a half-width left column with a long paragraph, paired button plus underlined link, divider, and 3 to 4 bottom stat columns beside a right media box. Let the headline and lead visual command the full width, center, or depth of the viewport, paired with at most 1 to 2 short lines of supporting copy (`<= 25` words), one clear primary action (or an immediate interactive stage), and zero bottom KPI or spec strip. Four non-split hero spatial directions to adapt or combine:
  1. *Centered monumental headline plus wide interactive stage*: a wide centered `<h1>` (70% to 92% width, optionally setting an inline cutout, visual tile, or animated token inside the `<h1>` line itself), 1 to 2 concise lines, and one CTA above a wide (80% to 100%) interactive workbench, preview, or lower stage visible above the fold.
  2. *Full-bleed photographic or living-canvas takeover*: edge-to-edge `min-height: 100dvh` from `top: 0` behind a borderless header, with display type and CTA placed in a high-contrast clearing.
  3. *Layered depth and foreground occlusion*: monumental edge-to-edge display lettering sitting behind a central cutout subject or interactive object via `z-index`, with title and primary action anchored along the lower horizon.
  4. *Wall-to-wall poster or corner-to-corner choreography*: oversized tightly stacked poster typography over bold chromatic color-blocking, top-edge painterly gradients, edge-bleeding graphic shapes, or diagonal corner-to-corner headline tension.
- **Expressive hero type and sustained pacing.** Kinetic hero typography (staggered line or word entrance, curved `<svg><textPath>` ribbons, subtle variable-weight or tracking response, inline animated tokens) must render visibly and legibly at rest (never stuck at `opacity: 0`) and honor `prefers-reduced-motion`. Carry the opening screen's visual conviction all the way to the footer instead of dropping into generic three-column card rows after screen one.

## Anti-slop filter

This is a filter, not a style. It says what not to ship when the model reaches for "designed" defaults. Any one tell is survivable; stacking them is what reads as AI-made on sight. If the brief explicitly asks for one, do it. Full list: `design/taste-skill.md` section 9.

- **No em-dash or en-dash as a separator anywhere visible.** It is the most common model tell and survives "use sparingly." Use a period, comma, colon, or hyphen. Always preserve user-supplied text verbatim.
- **No pre-heading eyebrows or decorative chips of any shape.** Start sections directly with `<h1>` or `<h2>`. Do not place `.eyebrow`/`.kicker` labels or `"Location · Batch · Status"` lines above headings, do not attach decorative non-interactive badges, chips, or category tags of any shape (rounded capsule or square bordered box) above headings, over images, or inside cards, and do not pad a hero bottom with a stat or metadata bar. Reserve bordered or capsule shapes for interactive controls or genuine semantic status cells in tables and API references.
- **No button walls or nested card cages.** Give each marketing or content section at most one primary CTA button (do not automatically pair every primary button with a second underlined link or ghost button unless the workflow needs two distinct actions). For mode, size, filter, or setting choices, use non-button selection controls (connected segmented toggle, tabs, radios, switches, `<select>`, or direct canvas interaction), never clusters of separate bordered buttons. Group with whitespace, `1px` dividers, or surface tint instead of cards inside cards.
- **No div-built fake product UI** on generic landings. Use a real screenshot, a generated image, or nothing. The exception is an animated HTML mock built from real component labels and real data.
- **No three equal feature cards, centered hero plus gradient blob, or AI-purple accent.** These are the model's defaults, so they are what every other generated page already looks like.
- **No Inter plus slate by default, no pure `#000`, no neon glow, no gradient headline text, no custom cursors.**
- **No filler copy or decorative numbering:** version eyebrows (`V0.6`, `BETA`), section numbers (`01`, `02`, `[ 01 / 04 ]`, Roman numerals unless steps are a real sequence), step labels (`Step 1/2/3`), synthetic `LIVE` dots, `SCROLL` cues, rotated edge text, locale and weather strips, "Quietly trusted by", "Elevate/Seamless/Reimagined/Unleash", stacked adjectives, or fourth-wall design commentary. Lead headings with user benefits rather than raw specs ("Lightweight shell", not "2.6 kg Cabin Mass"), and keep headlines whole without `<br><em>` italic splits.
- **No fake data:** "John Doe", "Acme", `99.99%`. Fake-perfect numbers read as invented. Quote real public figures from a named source or show nothing.
- **No decorative dots, hairline grids, or pills on photos** unless they carry meaning.
- **Rationed middle-dot**, at most one per metadata line.

## The five AI default looks

From Anthropic's `frontend-design` skill (Apache-2.0, ideas only): if your plan matches one of these without the user asking for it, change direction.

1. Warm cream background, serif display face, terracotta accent.
2. Near-black background with one acid accent color.
3. Broadsheet hairline rules with zero radius. It can be a deliberate product look for dense data screens; avoid it as the default on landings, where it reads as the model's editorial kit.
4. The SaaS kit of identical rounded cards with soft shadows.
5. ALL-CAPS eyebrows and middle-dot meta strings.

Two passes before you build. First write a compact plan: 4 to 6 named hex tokens, type roles, and an ASCII wireframe. Then review that plan against the brief and this list, and cut whatever is generic. Spend boldness in one place per page, not everywhere.

Pre-flight: run `taste-skill` section 14 plus this delivery audit before calling a page done:

- **Opening format fit:** content or workspace formats open directly into live content with no marketing hero; hero-led pages use a bold non-split composition bleeding to `y = 0` with `<= 25` words of supporting copy, one primary CTA, and no bottom KPI or spec strip.
- **Typography discipline:** at most 2 font families (`tabular-nums` instead of a 3rd monospace face), at most 3 distinct body sizes below the fold (4 only for an explicitly requested dense dashboard or table; hero `<h1>` and navbar wordmark exempt), consistent body size across paragraphs and lists, sentence-case UI labels, and zero `< 13px` text above the fold.
- **Zero decorative chrome:** sections start directly with `<h1>`/`<h2>`, zero decorative chips or badges of any shape, zero decorative heading prefixes or fake `LIVE`/`SCROLL` cues, at most one primary CTA per section (non-button controls for mode/filter/size choices), and zero nested cards.
- **Copy, motion, and rendered pass:** benefit-led whole headlines without `<br><em>` italic splits, zero em-dashes or spaced en-dashes in generated copy, explicit CSS transition properties (never `transition: all`), `prefers-reduced-motion` honored, and rendered screenshots inspected across desktop opening viewport, scrolled below-the-fold sections at desktop height, and `390x844` mobile for single-line nav, scrolled header separation, zero collisions, consistent hierarchy to the footer, and zero overflow or clipped display words.

## Scroll-film landing rules

Read `design/landing-scene-variety.md` before building multi-scene landings (`/login`, `/about`, or welcome routes) that tell the product story as a scroll-driven film.

- **Scroll is the playhead.** Motion is CSS sticky plus CSS scroll-driven animation, behind `@supports`. GSAP ScrollTrigger only when CSS cannot pin one scene. No Lenis, canvas frame sequences, Three.js, or video scrubbing. Why: CSS scroll timelines run off the main thread and degrade to a readable page when unsupported. The exception is a decorative WebGPU shader backdrop, which must still degrade to a static image.
- **Final state is the default state.** Without JavaScript, without scroll-timeline support, and under `prefers-reduced-motion`, every word and the CTA must be visible in document order. An observer that never fires must not hide the sign-up button.
- **Footage is real.** Live data comes from your own cached endpoint, never from a metered third-party API in the browser. Loading, empty, failed, stale, and ready are five distinct states. Mocks show only capabilities that exist.
- **Humans | AI toggle** on every landing when serving both audiences, with one shared agent data module feeding the AI view and `/llms.txt`.
- **Scene variety.** Adjacent cuts never share a layout family (stack, bleed, window, terminal, layered, poster, strip, pudding, control). Left-copy/right-mock twice in a row is a fail. Name each scene's family in the PR.
- **4 to 6 beats.** Open, hold, cut, close. A beat that restates an earlier one is deleted.

## Image generation

Use `design/imagegen/index.md` (OpenAI Image API through its CLI). Flow:

1. Decide what the prompt must lock: subject, composition, palette, lighting, what to exclude.
2. Generate two variations (`size`, `quality: high`, `output-format: png` or `webp`) into `public/` or a scratch dir.
3. Inspect the actual output files. Re-prompt on clipped subjects, muddy contrast, or text artifacts.
4. Keep only what wins. Compress for web delivery before committing.

## Brand, logo, and slide decks

- Brand system and token architecture: `design/design-system/index.md` (`token-architecture`, `primitive-tokens`, `semantic-tokens`, `component-tokens`).
- Brand boards and logo sheets as images: `design/brandkit.md`.
- Logos, icons, banners, social images, HTML decks: `design/design-kit/index.md` and `design/banner-design/index.md`.

## Video and 3D

- Scroll-driven product sites: `../scroll-film-site/SKILL.md`.
- Image-first comps before building: `design/image-taste-frontend.md`, `design/image-taste-art-direction.md`, `design/imagegen-frontend-web.md`, `design/imagegen-frontend-mobile.md`.
- Remotion, Three.js, R3F, and Spline rules live in `design/taste-skill.md` and `design/high-end-visual-design.md`.
