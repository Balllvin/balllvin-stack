---
name: research-notebook-ingest
description: >-
  Use when filing a paper, article, URL, PDF, or vendor note about open models
  (architecture, training) or about hardware (chips, memory, interconnect,
  local or edge devices) into a research notebook, with a short
  why-it-matters article.
---
# Research notebook ingest

Keep one notebook per topic: a **models** notebook (architecture and training recipe), a **hardware** notebook (chips, memory, interconnect, quantization, local or edge hardware), and a **harness** notebook (inference engines, agent loops, eval harnesses). This skill files into the first two.

## Route

- Model architecture, weights, or training paper: models notebook.
- Die, memory, interconnect, quantization, or a paper that sizes those: hardware notebook.
- A piece that argues both: file in hardware, and also send the source plus a short cut to models. Keep the hardware copy while it still supports a hardware argument.
- Inference engines, agent loops, eval harnesses: harness notebook, not here.

## Steps

1. Add the original as a source in the target notebook.
   - URL: add the link as a source and confirm it.
   - File: upload the PDF or document.
   - Pasted text: add it as a titled text source.
2. Write a short markdown article: what it is, what it claims, which numbers to trust, and why it matters (for the model itself, or for the chip).
3. Save it as a notebook file with a numbered slug, for example `12-mixture-of-experts.md`.
4. Do not invent numbers. Label paper-reported or vendor benches, and unconfirmed scoops, as such.
5. Run the how-to-write skill on every sentence, then how-to-write-paragraphs on anything longer than about four sentences. Ask: can I simplify this?

If the notebook tool fails, record the command you ran and what you wanted, and fix the tool before inventing a workaround that drops the source.
