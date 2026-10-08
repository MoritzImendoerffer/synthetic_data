# PCP-005: final pass (review run 2 + factual pass). Fix these, nothing else.

The factual pass found no factual error. These come from review run 2.

## A. Builder changes since your last render (no action beyond checking your text against them)
- Notes are now lettered in the order each table uses them (no "e)" without "d)"). If your prose
  cites a note by letter, compute it: `T.<builder>(...).marker_for("text of the note")`.
- Single-step tables drop their constant Step column (criteria change, methods by study, derivation).
- AMD-001's config title now reads "Fragments by non-reduced CE-SDS at every step, because SEC is
  biased in the capture and viral inactivation matrices".
- Use `T.sop_references(...)` for the procedures table (its type column is merged).
- The approvals table caption becomes the plain sentence "Synthetic record. Signatures are not
  applied." (no numbered caption; Section 13's reference to "Table 2" goes with it).

## B. Science (Q1/Q5)
1. Pool host cell protein is reported per mg of antibody. "A higher protein load puts more antibody
   on the bed, and with it more host cell protein bound to the antibody" and the steeper-slope
   sentence do not explain a rise in ng/mg, because antibody-bound host cell protein scales with the
   antibody. The expected direction (rising with load and with falling elution pH) is the A-Mab case
   study's observation: state it as that, and give only a mechanism that explains a per-mg rise
   (for example host cell protein bound to the resin rather than to the antibody, eluted at low pH,
   whose amount does not fall with load), or none.
2. "Some is bound to the antibody itself, and the wash does not displace it either, because the
   antibody stays bound to the ligand." Name the association the wash does not disrupt.
3. "As the load approaches the dynamic binding capacity, the mass transfer zone also reaches further
   down the bed, and impurity that the wash would otherwise remove is carried into the eluate." Say
   why, or cut the clause.
4. "The capture of Fc-bearing species and the low-pH hinge hydrolysis depend on bed height,
   residence time and elution pH …". Hinge hydrolysis depends on pH, time and temperature, not on
   bed height. Separate the two.
5. "Within the operating ranges of one run, leached Protein A is expected to be flat." In ppm (per mg
   antibody), a fixed amount leached per cycle falls as load rises. Correct the expectation. The
   claim that protease activity "rises while it is held" in a clarified harvest: state it as the
   expectation it is, once.
6. "Protein A does not separate aggregate from monomer, since both carry Fc." Qualify (aggregates
   bind with higher avidity and can be partly resolved on elution; under platform conditions the
   pool aggregate follows the load).
7. §6.5 "Aggregate and fragments are measured by SEC and acidic variants by icIEF at every sample
   point" against Table 5.1 (no SEC fragment row for hold samples) and §6.5's own nrCE-SDS on days 0
   and 7 against Table 5.1 "hold samples". Make Table 5.1 and §6.5 say the same.
8. "the hold study runs alongside the response-surface design": the two overlap by a few days only
   (Table 11.1). Say what is true.
9. "judging the pool against the drug substance limit would fail every acceptable run": reword.

## C. Criteria (Q4)
10. Cook's distance 4/n: give its basis or use the cut-off the campaign states.
11. The 90 % interval of the offset: give its basis in one clause (as PCMP-001 does).
12. Table 7.1: say one-sided for an upper criterion.

## D. Tables
13. Table 7.1: shorten the headers ("Attribute", "Statistic judged" with its meaning in a note) and
    move "none, no fragment result in the qualification" into a note. Merge the repeated
    "subtracted".
14. Table 8.2: replace the repeated long "How the value was set" texts with short entries and notes
    (e.g. "Platform^a)^", "Bound^b)^", "Platform, model not adequate^c)^").
15. Table 8.1/4.1: use "DS criterion" and "IAC" in headers where the column is narrow (both are in
    the Abbreviations table), and state the unit of the Increase column.
16. Table 5.1: drop the duplicated AMV or method column, so it fits without heavy wrapping.

## E. Readability (Q6/Q7), the clearest ones
17. The repeated glosses: "S-PA-RET, the retest of retained samples" (4×), "the method decision
    AMD-001 set nrCE-SDS as the method for fragments" (about 6×), "SEC reads part of the host cell
    protein in the Protein A pool as fragment" (3×). Give each once, then use the short name.
18. SOP numbers used alone (SOP-2007, SOP-2008, SOP-1001, SOP-1002, SOP-4001): give the procedure's
    name with it at first use in a section.
19. Cut: "RA-001 gives the scores and the rationale, and they are not repeated here.", "This
    assumption is recorded as item 1 of Section 12.", "The criteria below apply the acceptance
    criteria framework of PCMP-001 to this step.", the restated bed-height and lack-of-fit sentences.
20. "That argument is the bound, the runs behind it, and the reason …": say what the report must
    give, as a list, or cut.
