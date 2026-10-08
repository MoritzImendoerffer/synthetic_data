# PCMP-001: final pass (factual pass + review run 2). Fix these, nothing else.

## A. Factual errors (factual pass)
1. §7.8 "Designs executed before that date measured fragments by SEC. These are … Protein A, low-pH
   viral inactivation and cation exchange …". The cation exchange response-surface design ran
   2026-03-02 to 2026-03-27, across the decision date, and measured fragments by both methods
   (Table 7.3, note c). The SEC-only designs are the cation exchange screening design and the
   invalidated first anion exchange execution. The Protein A and low-pH inactivation response-surface
   samples were later retested by nrCE-SDS. Compute the lists from `method_plan.csv` and the DoE
   CSVs, and assert them.
2. Table 7.3 (builder) now shows aggregate by SEC at Protein A, where the designs recorded an SEC
   aggregate result on every run. Check your text against it.
3. §5 "Qualification compares … for the CQAs that have a criterion at the step … and for step yield."
   Step yield is not compared at the bioreactor or at low-pH inactivation, and fragments and viral
   clearance are not compared at any step (your own §7.1). Say what the qualification compares, from
   `sdm_qualification.csv`.
4. §7.5: rule 3 ("Otherwise the platform value stands.") renders as running text. Make it the third
   item of the list.

## B. Contradictions found by review run 2
5. Table 1.1 says harvest "forms no product-quality CQA", and Table 3.1 and §3 assign fragments to
   harvest. Make them agree.
6. "This plan set the rule before any Version 2.0 report applied it" sits beside sections that report
   the outcome of applying it (the bounds 40.4 and 4.76, seven criteria changed). The plan was
   reissued after the data. Say what is true: the rule was written into this plan before any step
   report used it, and this reissue also records what it gave.
7. "A step plan is approved before the first characterization run of its step." and "the step plan
   sets its value before the study is run". True of Version 1.0 approval dates, not of the Version 2.0
   criteria, which came after the studies (the reason INV-001 requires derivation from platform data
   only). Say which version each statement is about.
8. Table 7.1 note a) ("No downstream step changes the attribute") is applied to acidic variants at the
   low-pH inactivation pool and to aggregate at the cation exchange pool, while §5 says holds can form
   aggregate and deamidate. State it as what the derivation assumes, and say how holds are covered
   (the hold studies and their criterion).
9. "The documents of the package depend on each other in one direction." INV-001 led to this
   revision, which closes a loop. Reword.
10. The unmeasured offset: "These outputs carry no offset and are judged as the model predicts them."
    An offset that was not measured is unknown, not zero. Say that these outputs are judged as
    predicted because the qualification did not compare them, and that their representativeness
    rests on what each step plan states.
11. Residual DNA has a drug-substance criterion and three steps clear it, but no intermediate
    acceptance criterion and no reason for leaving it out. Give the reason (the data and the brief
    show whether DNA is a response at any step; if not, say it is tested on the drug substance only).

## C. Tables (owner's rule: merge repeated index cells, keep headers narrow)
12. The approval table loses its numbered caption: replace the caption line ": Approval record …
    {#tbl-appr}" with the plain sentence "Synthetic record. Signatures are not applied." (template
    change; the stray "Table 2" before Table 1.1 goes with it).
13. Table 1.2 (plan register): group the PCP and PCR rows of each step under one merged step cell
    (`T.frame`, merge the subject), and widen the columns so "(Step 5)" and the IDs do not wrap.
14. Table 3.1: order the attributes by category and merge the category cells (`T.frame`).
15. Table 4.1: the headers run together. Break them over two lines.
16. Table 5.2: use `T.sop_references(...)` (tables.py §14), which merges the type column, in place
    of `sop_table(...)`.
17. Table 6.1: use a two-level header ("Screening" and "Response surface" each spanning their
    columns) in place of repeating the words in five headers. `T.frame` takes a one-level header;
    build this one as a `CTable` directly (see `tables.py` for examples).
18. Table 7.2: widen the virus column so "XMuLV (enveloped)" does not break over three lines.
19. Table 8.1: keep the plan IDs on one line.
20. Table 9.1: keep study IDs and dates on one line (column widths, or a smaller font size).

## D. Two clear wording fixes (review run 2)
21. "instantiate" (Table 8.1 intro): a software word. Say "apply".
22. "predictive interval": the term is "prediction interval". Use it throughout.
