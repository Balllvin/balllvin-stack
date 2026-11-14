---
name: scroll-film-site
description: >-
  Use when building or enhancing a personal or portfolio site that should
  scroll like a movie (cinematic scrub), including custom cursor motion and
  a deploy to the owner's hosting account.
---
# Scroll-film personal site

Build a personal or portfolio site where scroll is the playhead. Not a video file. Pleasant pacing, fully responsive, progressive enhancement.

## Authority

1. CSS sticky scenes plus scroll-driven animation first. A timeline library only when CSS cannot pin or scrub.
2. Follow the repo's art-direction or taste skill. Don't reach for a generic frontend kit that fights that taste.
3. Official scroll-timeline skills when they are installed.
4. Catalog ideas only (yes / maybe): blur-fade, glare-hover, scroll-progress, a lagging pointer, noise, light rays. Reimplement in CSS or the timeline library. Don't paste another framework's motion primitives.
5. Honor `prefers-reduced-motion: reduce` — stills, same content order, no motion-gated calls to action.

## Camera ladder (stop at the first rung that holds)

1. Delete redundant scenes.
2. CSS: sticky scenes, `animation-timeline: view()` / `scroll()`, transform plus opacity only.
3. A scroll-trigger library only if CSS cannot pin or scrub one scene. Gentle scrub, linear ease, kill on unmount. Animate transform and opacity only.
4. Do not add a third-party smooth-scroll hijack, canvas frame sequences, a 3D hero, or `<video>` currentTime scrub.

## Scene grammar

- 4–6 scenes max. Adjacent cuts must not share the same layout family.
- Open, hold (pin plus scrub), cut, close.
- Pin pattern: a tall scroller plus a sticky full-viewport still.
- No whole-page mandatory scroll snap.
- Content must read with JavaScript off. No scroll hijack. No per-tick framework state on mousemove or scroll.

## Personal-site content (adapt per brief)

Typical beats: identity, what I build, the current product, links (the real profiles they gave you), a close call to action.
Links are real URLs only — never invent profiles. Ask for the real ones if they are missing.

## Cursor

A custom cursor with spring lag or glare on move is allowed as progressive enhancement. Keep the native cursor available for reduced-motion and touch. Prefer pointer listeners with animation-frame throttling, not framework state on every move.

## Stack defaults

- A modern web framework is fine.
- Deploy under the owner's hosting account, not a different team's.
- Coding follows the local coding default: implement, then a second review, and arm a checkup routine.

## Definition of done

- A live URL under the owner's account
- Scroll feels like a film (pleasant, not snappy)
- Responsive; reduced-motion stills
- Real links only
- Report the URL when it is live
