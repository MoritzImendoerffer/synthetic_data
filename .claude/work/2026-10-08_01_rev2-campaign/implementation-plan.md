# Implementation plan — Rev 2 campaign

35 tasks. The requirements are in `docs/next/rev2-campaign.md` and the repository state is in
`exploration.md`.

## Order and why

1. **Freeze first (TASK-001).** Everything after it changes what the current documents' helpers
   return. Rev 1.0 must be captured while it still grounds.
2. **Model (TASK-002 to 006).** Chronology, then the analytical model, the hold and fraction
   datasets, the two-sided acidic-variants capability, and the IACs. Every new draw comes from an
   independent RNG stream. Rev 2.0 then re-analyses the same experiments as Rev 1.0, and one test
   proves it.
3. **Tables (TASK-007)** run in parallel with the model. This is the one technical risk: the
   PDF twin and the crossref.
4. **Registry and authoring artifacts (TASK-008 and 009).** These encode the owner's rule
   decisions.
5. **Rebuild (TASK-010).** The committed Rev 1.0 DOCX are not re-rendered, so the repository
   stays green.
6. **Pilot (TASK-011 to 015).** INV-001, PCP-005 and PCR-005, then their annexes, then a **halt
   for the owner's reading**.
7. **The other 18 documents (TASK-016 to 033).** PCMR-001 goes last. Different documents may run
   in parallel agents, one agent per document.
8. **Full rebuild and ship (TASK-034 and 035).**

## What could go wrong

- **Drift.** A same-environment drift in deep decimals would break the byte-identity test.
  Capture the fixture in this environment before changing the model.
- **Cross-references.** A raw-LaTeX table with a Quarto crossref might not number. In that case
  emit the caption inside the LaTeX and write the reference as plain "Table N" text through a
  helper counter.
- **Size.** The annex re-anchoring dominates the cost. Each document's builder region is
  rewritten against the new text, never the reverse.

## What will not be attempted

- The DoE designs, factor ranges and viral-clearance-as-response are not changed.
- `nlp_reports` is not changed. It does not know the `INV` prefix, and that gap is recorded.
- The weak-claims branch is not carried forward in this unit.
