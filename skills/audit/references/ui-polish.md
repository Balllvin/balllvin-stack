# UI polish

Load when the mode is UI polish, or when the ask is to polish the app, test it at different widths, or do a touch and 3G pass.

Source: Emil Kowalski, 11 Nov 2026 ([post](https://x.com/emilkowalski/status/2120508498236596597)): test in the browser at different widths, with touch emulation, and on a throttled 3G connection; fix anything that looks broken or feels off; save a before and after screenshot for every fix; send a summary afterwards.

This mode is a visual pass in a real browser, not a test-suite run. Do not substitute existing Playwright e2e specs or smoke builds for walking the live UI across viewports.

## Apps and servers

Scope one app at a time. Inventory every reachable route from that app's router/app tree and its UI architecture doc, covering main screens, detail views, settings, and auth states.

Run against a local dev server or preview build on loopback (`localhost` / `127.0.0.1`). Never point a polish pass at production hosts or write production data. Prefer dev while iterating on a fix, and recheck on the production/preview build when the app has one.

## Matrix

Walk every inventoried route at each of these viewports (CSS pixels):

| Viewport | Why this size | Touch |
|---|---|---|
| `320x844` | Narrower than standard phone; catches overflow `390` tests miss | `isMobile: true`, `hasTouch: true` |
| `375x667` | Small phone (`iPhone SE` profile) | `isMobile: true`, `hasTouch: true` |
| `390x844` | Standard phone | `isMobile: true`, `hasTouch: true` |
| `768x1024` | Tablet portrait | `hasTouch: true` |
| `1024x768` | Small desktop / tablet landscape | no touch |
| `1440x900` | Desktop | no touch |
| `844x390` | Landscape phone (`390x844` flipped) | `isMobile: true`, `hasTouch: true` |

On phone and landscape-phone profiles, always enable `isMobile` / `hasTouch`. A narrow desktop viewport is not a substitute for touch emulation.

Throttled 3G uses Playwright's Slow 3G profile, applied with CDP `Network.emulateNetworkConditions` on a Chromium session:

```text
offline: false
downloadThroughput: 50000
uploadThroughput: 50000
latency: 2000
```

Walk each main route once at `390x844` (touch) and once at `1440x900` (desktop) under Slow 3G, and again at any width where a loading, empty, or error state looked wrong. Turn the throttle off before capturing steady-state layout screenshots for later widths.

Theme: if the app follows `prefers-color-scheme` (switch with `page.emulateMedia({ colorScheme })`), walk both schemes at `390x844` and `1440x900`, and at any width where a defect is theme-specific. If an app is single-theme, record that in the report and skip the other.

## What counts as broken or off

Fix it when you can see it or measure it in the browser:

- Horizontal overflow or unexpected page-level horizontal scroll (`documentElement.scrollWidth > clientWidth`; also check fixed shells and panes, as in [playwright-interactive.md](../../ui-ux/references/playwright-interactive.md))
- Clipped or overlapping text
- Tap targets under `44px` on a touch profile
- Affordances that exist only on hover and cannot be reached with touch
- Layout shift after late content or webfonts
- Missing loading, empty, or error states on the Slow 3G profile
- Spinners that never resolve
- Janky or missing transitions (respect `prefers-reduced-motion`)
- Missing focus states
- WCAG 2.2 AA failures: unlabeled controls, keyboard traps, focus order, missing skip link, contrast under `4.5:1` for body text or `3:1` for large text, screen-reader unreadability of dynamic or async content, missing reduced-motion handling
- A raw provider error, URL, or HTTP status code shown to a person

Taste, tokens, and latency bars are owned by [ui-ux](../../ui-ux/SKILL.md), [TASTE.md](../../ui-ux/TASTE.md), [BEHAVIORS.md](../../ui-ux/BEHAVIORS.md), and [react-performance.md](../../ui-ux/references/react-performance.md). Do not let a polish fix regress page-load budgets.

## Fixes and screenshots

Fix the shared owner (a layout primitive, a shell, a token), not a one-page patch. Root cause only. Fix forward.

For every fix, take a before screenshot and an after screenshot at the same viewport, touch or desktop profile, network profile, and color scheme using `page.screenshot()`. Store scratch screenshots outside the git tree (never commit polish screenshots into the repository unless requested). List every fix and screenshot path in the PR body:

```text
Fixes:
  <fix-id> - what was wrong, where (route and component), widths and profiles, before path, after path.
Left: defects you saw and did not fix, with why.
```

After a fix lands, re-walk the affected routes across the matrix (including Slow 3G when the defect involved loading or pending states) and keep the after shot only when it still looks right.

Close dev servers, preview servers, and browsers by exact PID and remove temporary state when done.
