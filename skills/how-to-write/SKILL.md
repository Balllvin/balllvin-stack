---
name: how-to-write
description: >-
  Cut AI tells from any writing. Must always apply. This is the unslop skill.
  For drafts longer than about four sentences, also run how-to-write-paragraphs.
  Do not unslop the author's own register.
---
# Unslop

Edit text to remove AI patterns and add human voice.

Source: [pstack/unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)

For anything longer than about four sentences, run the how-to-write-paragraphs skill after this. Unslop is the sentence. That skill is the piece.

## Process

1. Scan for the patterns below.
2. Rewrite. Preserve meaning, match intended tone.
3. Add soul (see next section).
4. Self-audit: "What still looks generated?" Fix remaining tells.
5. If the draft is longer than about four sentences, run the paragraph skill: unity, given-new, handoff, one gotcha max.
6. Do not "clean" the author's register. Fragments, hedges, tickers as nouns, swearing, run-ons, parentheses, "I believe", a PS, stay if they are how the person talks.

## Adding soul

Removing patterns is half the job. Sterile, voiceless writing is just as obvious.

- **Have opinions.** React to facts instead of neutrally listing pros and cons.
- **Vary rhythm.** Short sentences. Then longer ones that take their time. Mix it up. A run-on is allowed when two facts have to stay in one breath.
- **Acknowledge complexity.** "Impressive but also kind of unsettling" beats "impressive."
- **Use "I" when it fits.** First person isn't unprofessional. I is process (a PS, a bet, a product you actually use).
- **Let some mess in.** Perfect structure looks machine-made.
- **Be specific.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am."

Do not fake humanity with slang, typos, or emoji. That is a different tell. Keeping the author's existing slang is not faking it.

## Author register (do not unslop this)

Unslop is for generated tells. It is not a teacher.

Keep, when they are already the voice:

- their hedges and swearing
- a ticker as a noun
- "I believe" / "I'm willing to take that bet"
- a fragment as a verdict
- parentheses for an aside
- a PS at the end

Do not sand those into "clean prose." The author's posted longform is the check: if a pass would have deleted a hedge, a running metaphor they earned, or a PS, the pass is wrong.

## Patterns to detect and fix

### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Listing media outlets without context. Pick one, say what was said.
3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
4. **Promotional language.** "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Also cut when stacked or figurative: realm, advancements, aligns, meticulously, seamlessly, cutting-edge, transformative, multifaceted, paramount, navigate, invaluable, deep dive. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features", "refers to". Just say "is" or "has".
9. **"Not just X, but Y."** State the point directly instead.
10. **"It's X, not Y" / "Not X, but Y" / "X rather than Y."** Same family as 9. Contrast-reframe that swats a misconception the reader never had. State the claim once. Name the rejected alternative only if someone actually chose it.
11. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
12. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
13. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

### Style

14. **Em dash overuse.** Avoid em dashes. They are an AI tell. Periods, commas, and normal parentheses ( ) are fine. Do not ban parentheses. Do not swap an em dash for a fake cousin ("on the other hand", a second "it's X not Y"). An aside in ( ) is how many people write.
15. **Colon overuse.** Colons are fine before a list or example. Not as mid-sentence connectors.
16. **Boldface overuse.** Don't bold every proper noun or acronym.
17. **Inline-header lists.** The tell is a bold label and colon that restates the line. Convert those to prose.
18. **Title case headings.** Use sentence case, unless the author's posted headings already mixed it. Match the author, not a style guide.
19. **Decorative emojis.** Remove from headings and bullets.
20. **Curly quotes.** Replace with straight quotes.

### Communication artifacts

21. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
22. **Cutoff disclaimers.** "While specific details are limited..." Find sources or remove.
23. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.
24. **Reader-steering.** "Here's what's interesting." "The key point is." "Notably." "It is worth noting." Put the fact first.
25. **Gotcha cadence.** "Here's the kicker." "Plot twist." "Let that sink in." "Read that again." One real turn per piece, as a fact, not a drumroll.
26. **Leftover machine markup.** Citation chrome, INSERT_SOURCE_URL, [Your Name], fenced wikitext. Never ship it.

### Filler

27. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
28. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may". Author hedges stay.
29. **Generic conclusions.** "The future looks bright." State specific plans or facts. Also kill the recap close that is just the intro again.

### Jargon

30. **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. Pick the concrete word. A snowball is allowed when compounding is the hard object. One fable.

### Plain speech

31. **Say what it does, not how it feels.** Name the mechanism or a number. If the sentence could appear unchanged in another project's docs, cut it.
32. **Mixed length, not equal punches.** Split a generated dense sentence. Do not split an author run-on that is doing one breath.
33. **Active voice.** Prefer it. Passive is fine only when the actor is unknown or genuinely doesn't matter.
34. **Cut adverbs, or use a stronger verb.**
35. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help".

### Extra tells that are not unslop cousins

36. **Vague association.** "in connection with", "associated with" where of / for / by / caused by would do. Name the relationship.
37. **Tour-guide openers.** "In this article we will explore", "In an era where", "In today's rapidly evolving". First sentence makes a claim this piece can defend. If you can swap the noun and the opener still works, rewrite it.
38. **Notability metacoverage.** "independent coverage", "trade publications", "active social media presence". One source, what it claimed, date. Never write about the sources to prove the subject is real.
39. **Regression to the mean.** Specific odd facts sanded into generic praise. Keep the weird fact. Cut the statue sentence.
40. **Ambient niceness.** Polite, upbeat, inoffensive weather. Irritation, doubt, boredom, and preference are allowed. End on a fact or a choice, not a wistful closer or "embrace innovation responsibly."
41. **Do not swap a tell for a cousin.** "on the other hand" for "moreover", "it's X, not Y" for "not just X, but Y" is the same machine. Parentheses are not a cousin of the em dash.

## First-reader apparatus

Do not add a sandwich table, a "who is they" glossary, or a scoreboard unless the author asked for that pass. A strong posted piece often wins with one cash path and one earned metaphor, not ten labeled figures. Teach the reader with the example, not with a legend.

Quote is an exhibit. Paste it. The next line is new (a leftover, a calculation, the next fact). Do not paraphrase the quote before it or after it.

## Apply order

1. This skill (unslop plus the extras above). Author register stays.
2. How to write paragraphs, if the draft is longer than about four sentences.
3. Kill leftover gotchas. One contrast is enough.
4. For the author's longform, also check it against a piece they already published and liked.
