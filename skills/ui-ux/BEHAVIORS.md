# Behavioral Primitives and Interaction Architecture

Use with `SKILL.md`, `TASTE.md`, `CRAFT.md`, and the app's UI architecture doc.

Adapted from the architectural concepts of `vercel-labs/ui` (`@ui-sdk/core`, Apache-2.0). Build your headless primitives in-house as small SSR-first islands (`data-island` roots mounted by one shared kernel) rather than pulling in heavy client widget libraries.

## Zero-dependency and supply-chain governance

Every external dependency is supply-chain attack surface and maintenance lock-in. Keep runtime dependencies minimal across JS/TS, Python, and compiled backends:

1. **No new runtime dependency without a written reason:** Never add a runtime dependency to `package.json`, `requirements.txt`, or `Cargo.toml` without a written technical justification and a monotonic dependency budget check. Keep test-only tooling isolated to dev/test manifests.
2. **In-house replacement and permanent removal:** Keep UI primitives, icons, stores, schemas, Markdown rendering/sanitization, overlays, charts, tables, and service workers small and owned in-house when practical. Every replacement slice proves parity with tests, deletes the package from both manifest and lockfile, and ratchets the dependency budget down.
3. **Exact pins:** Pin runtime dependencies to exact immutable versions (`1.2.3`, `==1.2.3`, `=1.2.3` in Cargo). Avoid open `^` or `~` range specifiers in production manifests.
4. **Lifecycle-script blocking (`--ignore-scripts`):** Run `npm ci --ignore-scripts` in CI, local validation, and container builds wherever builds allow it so transitive `postinstall` scripts cannot execute silently.
5. **Lockfile review:** Any PR touching a lockfile must audit the diff for new transitive packages, install scripts, unexpected tarball URLs, or checksum changes before merge.

## Headless kernel contract

Separate interaction state, ARIA wiring, focus movement, dismissal, and DOM positioning from app styling. Visual tokens stay in the app's CSS variables and architecture doc; behavioral modules emit zero inline visual styles and import no CSS palette classes.

- **Single primitive schema:** Define each shared widget behavior with typed `options`, internal `state`, reactive `live` / `direct` attribute bindings, named `slots`, imperative `api`, and an `agent` descriptor.
- **Fine-grained live attributes:** High-frequency state such as `data-highlighted` and `data-modality` updates the target DOM attribute directly via subscriptions without re-rendering list trees.
- **Controlled and uncontrolled parity:** Support `value` / `defaultValue`, `open` / `defaultOpen`, and `on<Key>Change(next, details)`. Warn in development when a component flips between controlled and uncontrolled across renders.
- **Change details and cancellation:** Every change callback receives `{ reason, event, source, cancel(), canceled }`. `source` distinguishes `"mouse"`, `"touch"`, `"pen"`, `"keyboard"`, `"virtual"`, `"programmatic"`, and `"agent"`. Listeners may call `details.cancel()` synchronously to veto a state transition before commit.
- **Strict teardown:** Every listener, layer registration, timer, scroll lock, and observer cleans up deterministically on unmount and survives strict double-mount cycles.

## Data-attribute and composition grammar

Communicate behavioral state to CSS exclusively through presence attributes and layout attributes. **Never encode state in combined `data-state="..."` strings or positional sibling selectors.**

| Attribute group | Allowed attributes |
|---|---|
| Presence state (boolean) | `data-open` / `data-closed`, `data-checked` / `data-unchecked` / `data-indeterminate`, `data-pressed`, `data-selected`, `data-highlighted`, `data-disabled`, `data-readonly`, `data-required`, `data-invalid` / `data-valid`, `data-focused`, `data-pending` |
| Presence motion (boolean) | `data-starting-style`, `data-ending-style` |
| Valued layout and input | `data-side`, `data-align`, `data-orientation`, `data-modality="keyboard" \| "pointer"` |
| Structural slot | `data-slot="<component>-<part>"` |
| Geometry CSS custom properties | `--anchor-width`, `--anchor-height`, `--available-width`, `--available-height`, `--arrow-offset`, `--transform-origin` |

Composition rules:

1. Use explicit `render` element or function composition instead of polymorphic `as` props.
2. Yield author-supplied `id`, `aria-label`, `aria-labelledby`, and `autocomplete` over generated defaults, merging `className`, `style`, refs, and event handlers without overwriting user handlers.
3. Prefer `aria-disabled="true"` over native `disabled` on buttons, menu items, and async triggers so keyboard users can still inspect disabled controls.

## Interaction foundations

Build every interactive island on one shared foundation:

1. **Unified overlay layer stack and top-layer popups:** Register every modal dialog, sheet, drawer, popover, menu, combobox popup, and tooltip in one shared layer stack (`pushLayer`) instead of ad-hoc `document.addEventListener("keydown")` / `"mousedown"` handlers. Support CSS Top Layer (`popover="manual"` + `::backdrop`) with measured anchor positioning and safe fallback.
   - Explicit `modal` modes: `true` (inert outside + scroll lock + focus trap), `"pointer"` (outside pointer blocked, keyboard tab exits), `"trap-focus"`, and `false` (modeless floating surface).
   - Structured dismissal: `dismissible` boolean plus `onDismissAttempt` feedback (for unsaved forms) rather than silent drop or swallowing Escape globally.
   - Structured focus return chain on close: explicit `finalFocus` -> trigger element -> pre-open `activeElement` -> parent overlay -> nearest DOM survivor, respecting `"unless-moved"` if focus already relocated intentionally.
   - Persistent alert layer: P0/P1 alert notices stay above modal layers and remain interactive when background content is inert.
   - Adaptive phone presentation: popovers and pickers accept `presentation: "auto" | "popover" | "sheet"`, upgrading to swipe-dismissible bottom sheets below coarse/phone breakpoints while preserving state and focus return.
2. **Modality separation (`data-modality`):** Track `"keyboard"` vs `"pointer"` on interactive widgets and root containers. Paint virtual highlight chrome (`[data-modality="keyboard"] [data-highlighted]`) and keyboard navigation cues only in keyboard mode so pointer movement never fights arrow selection and stale focus rings clear on click.
3. **Roving focus and focus recovery:** Composite widgets (`listbox`, `menu`, `menubar`, `tabs`, `radio-group`, `toolbar`, `tree`, `grid`) expose a single `Tab` stop and move focus with Arrow keys, `Home`, and `End` (respecting orientation, RTL direction, disabled items, and Shift-selection guards). When the active item disappears after filter/delete/reorder, focus recovers deterministically to the adjacent survivor or widget container instead of falling to `document.body`.
4. **Shared listbox, filter, and range selection:** Select, Combobox, Autocomplete, Command Palette, Tree Actions, and MultiSelect share one collection/filter/virtualization engine (including `hiddenUntilFound`, chat `stickToBottom`, inline editing, and `Shift+Arrow` range + clipboard TSV helpers).
5. **Motion presence:** Popups, sheets, and disclosure panels mount with `data-starting-style`, stay mounted with `data-ending-style` and `inert` until real `getAnimations()` (including `::backdrop`) settle, and skip waiting under `prefers-reduced-motion: reduce`. Interruptible reopen clears closing state cleanly.
6. **Async actions and double-submit guard:** Action triggers accepting async handlers expose `data-pending` and `aria-busy="true"`, ignore repeat presses/submits synchronously until settled, announce `"Loading"` politely after 1000ms for genuine waits, and hold failures in recoverable error state without closing the enclosing sheet or losing draft input.
7. **Forms and native participation:** Custom switches, checkboxes, radios, selects, and sliders sync hidden native inputs so native `<form>` serialization (`FormData`), `form.reset()`, and `<fieldset disabled>` inheritance work with SSR.
8. **Layer-aware shortcuts and typeahead:** Global hotkeys (`"mod+k"`, sequences like `g p`) check the active layer stack and text-entry focus automatically rather than rolling custom input checks per feature. Select/menu lists share printable character typeahead and check accessible names in development.
9. **Direct manipulation and accessible reorder:** Drag, reorder, tree indent/outdent, and swipe actions provide both pointer physics and keyboard equivalents (`Space`/`Enter` + Arrow move) with polite screen-reader status announcements.
10. **Direction and RTL readiness:** Navigation keys (`ArrowLeft` / `ArrowRight`) and placement (`inline-start` / `inline-end`) read computed element `dir` without requiring a top-level context provider.

## Agent-ready control surface and safety

Every interactive view is inspectable and drivable by local automation and tests without brittle DOM scraping:

- **Registry integration:** Shared UI primitives register live interactive instances (type, accessible label, row context, state, available actions) so the page surface exposes structured `snapshot()`, `act({ steps })`, and `query()` operations. Never build a duplicate second agent command protocol.
- **Traceable source:** Agent-driven state mutations pass `source: "agent"` through `ChangeDetails`, allowing sensitive flows to inspect, log, or veto via `details.cancel()`.
- **Mandatory safety attributes:**
  - `data-agent-confirm="<plain sentence>"` on irreversible, destructive, financial, permission, or admin-approval controls (`Delete`, order submit, account link, request approval).
  - `data-agent-secret` on API keys, ingest tokens, webhook secrets, credentials, and raw token fields so snapshots redact their values cleanly.
  - `data-agent-hidden` on decorative or internal chrome excluded from agent discovery.

## Required verification per interactive primitive or surface

1. **WAI-ARIA pattern check (`checkPattern`):** Verify roles, required ARIA states, live `aria-controls` / `aria-labelledby` targets, single tab stop per composite, Arrow / `Home` / `End` / typeahead / `Enter` / `Space` / `Escape`, and zero focus drops to `document.body`, `aria-hidden`, or `inert` elements.
2. **SSR safety (`checkServer`):** Render every shared primitive without `window` / `document` globals and confirm open-before-hydration stability.
3. **Direction safety (`checkDirection`):** Verify RTL arrow mirroring and logical inline placement on menus, tabs, toolbars, and trees.
4. **Agent readiness test:** Assert structured discovery (`snapshot()` finds labeled controls, redacts `data-agent-secret`, flags `data-agent-confirm`) and programmatic drive (`act()` mutates state with `source: "agent"`).
5. **Mutation sanity and dependency checks:** Break a keyboard handler, focus return, or veto guard during development to verify the suite catches it, then restore and run desktop/mobile Playwright checks plus slop and dependency budget checks.
