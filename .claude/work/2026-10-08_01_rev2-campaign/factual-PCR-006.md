# Factual check of PCR-006 Version 2.0 (draft text of 2026-10-10)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed, every error
kept). Scratch scripts s1 to s9 (read-only, through doe_report, _pcpkg, adequacy and iac). Most numbers are
right; the errors are in what they are said to mean.

1. §7.7 "which this bound widened from 9.30 to 6.46 % HMW": a priori 9.30; the cation exchange bound tightened it
   to 6.32; this step's bound (0.5586) widened it to 6.46 (iac.csv tightened and widened). Fix: "widened from
   6.32 to 6.46 % HMW, after the cation exchange verification had tightened it from its a priori 9.30 %".
2. §7.5 NOR decisions: the hold-time NOR as characterized was 60–120 min (90 min its centre, not its lower
   edge); the narrowing to 90–120 min is never stated; the first-stage set-point 105 min is never given; the
   temperature NOR 20–23 °C belongs to the first step (the first-stage edge pH 3.54 holds only at 20 °C). As the
   config holds them: (1) hold-time NOR 90–120 min and temperature NOR 20–23 °C (owner's option C,
   2026-10-08); (2) pH set-point 3.40 with NOR 3.30–3.50, hold-time set-point 105 min, the middle of 90–120;
   (3) hold-time NOR 100–120 min with set-point 110 min (decision 3b), which triggered S-VI-WC.
3. F3, §5.3.2, §11 item 3 overstate the influence analysis ("no conclusion changed"): with run 5 deleted the
   XMuLV NOR-propagated PARs move (pH 3.2–3.68, hold 72–180, temperature 15–25, no longer set by the claim), and
   the temperature effect on XMuLV (0.57, p = 0.036) depends on run 5. What holds under every deletion: the NOR
   in force inside every PAR, the claim met over it, the decision to move the NOR, the classes. Limit the claim
   and state the run-5 dependence.
4. Departures in neither register: 4a input-pool samples (PCP-006 §5.3, §5.4, §6.3) [registered since:
   DEV-006-04]; §4.3 "Every output was measured on every run" conflicts; 4b a widening on a model failing
   criterion 4 vs PCP-006 §7.4 rule 2 (all four §7.1 criteria) [PCP-006 is being re-opened to state the first
   three, as PCMP-001 §7.5]; 4c the near-equivalent model comparison has no entry [it is the sensitivity of the
   model selection, PD-006-04]; 4d the risk argument for the widening does not say who bears the risk
   (PCMP-001 §7.5 item 1); 4e adjusted R² not reported (PCP-006 §5.5); S-VI-UNI acidic variants compared with the
   designs, not the S-VI-SDM set-point runs; "recorded within PD-006-05" (the entry records the study only);
   PD-006-07 "Done" sets residual trends against the criterion, the report against the residual SD; the fragment
   model not reported against criterion 4 (runs 4 and 12 exceed).
5. §1.4 item 4 "have a model that meets the adequacy criteria" vs F3 and §5.3 (both fail the fourth).
6. §13.2 PD-006-04 attribution: this step's bound is 0.5586 selected vs 0.5584 full, so the bioreactor shift
   (6.46 vs 6.19) comes from the cation exchange bound (1.40 vs 1.35-fold); omitted: this step's own aggregate
   criterion 7.02 % with CA3, 6.75 % without; the exact-fit acidic model would have widened the bioreactor
   acidic upper limit to 39.6 % without CA3 (39.0 % with).
7. "no conclusion of this report rests on a rule chosen after the data" is false (CA3 adopted 2026-09-15; the
   influence analysis; the ranges in force); name the rules fixed before their results (fold rule and run counts
   of S-CEX-VER and S-VI-WC) and state the limitation for the rest.
8. The Version 1.0 comparison mixes NORs: under the NOR as characterized no XMuLV PAR exists (lowest mean 6.31 at
   pH 3.5, 60 min, 19 °C); PCP-006 §8 rule 4 says "reports that no PAR exists"; the design space moved too
   (Version 1.0 79.9 %, bounded by aggregate; Version 2.0 63.9 %, bounded by XMuLV).
9. Chronology: "Their results were known when the set-points and NORs of this revision were decided" vs §7.5
   (S-VI-WC made because the NOR had been revised; S-VI-OFAT and S-CEX-VER tested pH 3.40 after the first
   decision).
10. The NOR-propagated PAR for XMuLV uses the 9 NOR combinations and draws nothing (PCMP-001 §6.4,
    par_nor_propagated); §3.5 and §7.4 describe draws; Figure 7.1 labels [builder fixed: "Others at their NOR
    combinations", "range of mean predictions over the NOR combinations"].
11. Table 7.13 "Confirmed" for fragments vs the text "confirms nothing on its own" [the builder follows PCMP-001
    §7.5, confirmation on the point prediction: say so and state the limitation of the model].
12. Figure 5.4: the claim contour rises from bottom left to top right, not top left to bottom right.
13. §5.3.1 "Three of them carry a squared pH term and a squared hold-time term" (one lacks hold time²).
14. §7.5.1, §7.5.3: "Over the hold times within the NOR in force" covers 0–120 min (within 100–120: 1.95–2.14 %,
    0.94–1.08 %, 19.8–20.6 %); values printed at scale-down scale though "judged at manufacturing scale"
    (S-VI-OFAT 1.48–2.12 and 19.56–20.36; S-VI-WC 2.05–2.07 and 19.65–20.58 at manufacturing scale).
15. §7.6 acidic variants 20.6 % (scale-down) vs Table 7.12 20.3 % (manufacturing).
16. §11 "Aggregate and fragments grow with ... the temperature": no result shows a temperature effect on
    fragments.
17. "For every output ... the interval contains both values" and "chose the raw scale for every output": not
    acidic variants (no Box-Cox interval).
Minor: fragment results beyond the 18 design runs; fragments and acidic variants judged on measured results;
term counts with and without the intercept; §7.2 interval at the worst corner vs over the NOR; "none of them
was run at settings inside the NOR in force" (vacuous); "wider than the slice" (reversed); "bound any effect of
pH within about 0.03" (linear term only); residual SD 0.390 vs pure error 0.381; "did not differ" → "not
detected"; "within 0.017" (0.0174); S-VI-UNI2 aggregate 2.03 vs 1.88 % not discussed; "because each acted"
(plan: "expected to act"); §10 item 3 omits the S-VI-WC fragment failure; Table 5.10 "Adequate: Yes" with runs
above 4/n; Table 3.1 note on acidic variants; ICH Q11 not in the references, Q10 year; Conclusion 1 "meets its
claim of 6.60"; §7.3 hold material set-point; Table 7.2 mean vs the 2.10 % limit; Table 5.9 "Met: Yes" for
inadequate fragment models; S-VI-WC "harshest combination within the PAR" [canon relabelled 2026-10-10].
D-001: present as registered (Table 7.4 "PAR (set-point)" at the design centre; Figures 7.1/7.2 left panels
"At set-point (others fixed)"); not reconciled. Keep.
