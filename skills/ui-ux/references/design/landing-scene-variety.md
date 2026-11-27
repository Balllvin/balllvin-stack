---
name: landing-scene-variety
description: >
  Multi-scene landings must change layout family at every cut. Use when
  editing login or marketing landings, or when a scroll film repeats
  left-copy/right-image.
---

# Landing scene variety

Scroll can be a film. Adjacent cuts still cannot share a layout.

## Fail

Two scenes in a row that are copy on one side and a mock on the other. A 50/50 split hero template (left H1, long paragraph, paired buttons, divider, and bottom stat columns beside a right media box). A stack of the same card. A hero that is already the next scene.

## Layout families

Pick a new family for each cut. Do not reuse the previous one. "Proof" means a real product mock, screenshot, or still.

| Family | Shape |
| --- | --- |
| Stack | Full-viewport type. Control or proof under it. No side column. |
| Bleed | Proof fills the viewport. Copy sits on the proof. |
| Window | Proof is a centered frame. Copy above or below, not beside. |
| Terminal | Proof fills. Copy docks the opposite corner from the last bleed. |
| Layered | Edge-to-edge display type sits behind a central foreground subject or frame (`z-index`), with title and CTA anchored along the lower horizon. |
| Poster | Huge type. Proof is a band or a small frame. |
| Strip | Several proofs in one row. One heading. |
| Pudding | Sticky heading. Stepping copy. No product frame. |
| Control | The interactive control is the scene. |

## Check

Name the family of each scene in the PR. If two neighbors match, restyle one or delete one.

## Proof and fill

- A mock uses current product labels and structure. If the product merged two sections, the mock shows one.
- A screenshot must load cleanly from `public/`. Never lay a copy box over a screenshot.
- A `100dvh` sticky mock with eight lines of copy is empty. Fill the mock, or do not pin that tall. Give each pinned step 60 to 70dvh of scroll without hairline dividers between pinned steps.
- If using a cursor spotlight, keep one fixed page-wide layer rather than nested spotlights inside boxes.

## Proof review

Open every mock and still before opening a PR. Say in one line what each shows. Fail if proof is:
- Sign-in or Create-account marketing instead of the product work itself
- The landing page photographing itself
- A broken image or an empty frame
- Cropped off the work, out of focus, or showing an outdated product layout
- Private secrets, passwords, or real customer data (always use a clearly labeled seeded demo)

## Viewports

Before PR, screenshot the live landing (opening viewport and scrolled below-the-fold sections) at:

- `390 x 844` (phone)
- `1280 x 800` (laptop)
- `1440 x 900` (desktop)

Verify single-line desktop navigation, clean scrolled header separation, zero text or visual collisions, consistent type hierarchy to the footer, and zero horizontal overflow or clipped display words.

On the phone:
- Type wraps inside the viewport. No `clamp` floor above `3.25rem` on a heading.
- No `100dvh` proof or overlay copy; copy sits in document flow under the proof.
- Hero is not an empty column with the dock at the bottom.
