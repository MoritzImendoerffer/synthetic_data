# TASK-004 procedure — re-author `PCR-003` a third time, as a DRAFT

**Follow `../../2026-08-17_01_register-second-round/procedures/TASK-006.md` top to bottom, with
the substitutions below.** That file (and its TASK-005 it inherits from) is the tested procedure;
this file only says what differs in round three.

## Substitutions

| there | here |
|---|---|
| pre-rewrite dir `2026-08-17_01_register-second-round/pre-rewrite/` | `2026-08-18_01_register-third-round/pre-rewrite/` |
| `git diff --quiet f06f1a7 -- …` | `git show e7a4768:pc_package/PCR-003_bioreactor.qmd \| diff -q - <copy>` (round two is `e7a4768`) |
| "the previous revision sat at 8.0 % `, so `, 0.9 % initial connectives, chaining 30.7 %, `pct_under_15` 22.7 %" | "the previous revision sat at 0.0 % `, so `, 4.0 % initial connectives, chaining 46.1 %, copula 25.7 %, `pct_under_15` 19.5 % — and at **22.6 %** `, and ` + second clause, **4.3 %** `, not `, **35 %** passive, all three of which are what the reading of round two named" |
| `build_brief.py PCR-003` | `uv run --extra discourse python authoring/build_brief.py PCR-003` (so §5d carries the passive row) |
| the four additions in §3 of that file | keep all four; **add a fifth**: "The three sentences of the round-two report that said 'the factors that screening retained' are the ✗ example the guide now carries at §2d. A study, design, model or process is never the agent of retain/carry/identify/select; write the passive the sources would write. This is a substitution: search your draft for `screening retained`, `the design carries`, `the model identifies`." |
| | **and a sixth**: "The two new search strings: `, and ` followed by `the` / `this` / `both` / `it` / `each` starting a second clause, and `, not `. `check_style.py` prints both back on every render as `', and '+clause` and `', not '` beside the packing figures. The passive figure is in the brief only; it is a band, and the sources sit at 54–60 %. Do not write passives to hit a count; write them where the sources would." |

## The brief text to hand the agent

The previous unit's TASK-005 §3 brief, with the report class, `report_doe`, and the six additions
above. Do not paraphrase the rules; hand it the strings.

## Extra checks in §4 of that file

```bash
grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' pc_package/PCR-003_bioreactor.DRAFT.qmd   # 0
uv run python authoring/check_style.py pc_package/PCR-003_bioreactor.DRAFT.qmd | grep "clause packing"      # copy the WHOLE line into outcome
```

## Do not

Re-author `PCP-003`. It is the control column and stays at round two.
