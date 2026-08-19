# Run 1 — the commands by which the author measured its own draft

Extracted from the agent transcript by tool-input grep (the transcript itself is not read). Command index in the agent's sequence of 115 bash commands.

## [20]
```
grep -n "BANNED\|GATED\|^TIC\|def gate\|def main\|em_dash\|semicolon\|colon" authoring/check_style.py | head -50
```

## [21]
```
sed -n 96,230p authoring/check_style.py
```

## [31]
```
sed -n 230,345p authoring/check_style.py
```

## [67]
```
cd /home/moritz/github_repos/synthetic_data/pc_package && uv run python -c "
import sys,os,re
sys.path.insert(0,'/home/moritz/github_repos/synthetic_data/authoring')
import check_style as cs
t=cs.prose_from_qmd('PCR-007_cex.DRAFT.qmd')
from collections import Counter
c=Counter(w for w in re.findall(r'\b[a-z]+(?:-[a-z]+){2,}\b', t.lower()) if w not in cs.HYPHEN_ALLOW)
print(c)
"
```

## [72]
```
uv run python authoring/check_style.py --review pc_package/PCR-007_cex.DRAFT.qmd 2>&1 | head -60
```

## [73]
```
grep -n '"paren"\|paren.*per1k\|rather_than' authoring/check_style.py | head
```

## [74]
```
uv run python - <<'PYEOF'
import sys, re
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
sents = cs.sentences(t)
print("=== ', so ' sentences ===")
for i, s in enumerate(sents):
    if cs.SO_MID.search(s):
        print(f"[{i}] {s}")
PYEOF
```

## [75]
```
uv run python - <<'PYEOF'
import sys, re
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
sents = cs.sentences(t)
print("=== ', and ' + clause  (%d) ===" % sum(1 for s in sents if cs.AND_CLAUSE.search(s)))
for i, s in enumerate(sents):
    if cs.AND_CLAUSE.search(s) and not cs.SO_MID.search(s):
        print(f"[{i}] {s}")
print()
print("=== rather than ===")
for i, s in enumerate(sents):
    if re.search(r"\brather than\b", s):
        print(f"[{i}] {s[:160]}")
PYEOF
```

## [76]
```
cat > /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad/reflow.py <<'PYEOF'
"""Unwrap prose paragraphs of a .qmd, apply edits, rewrap. Code fences untouched."""
import re, sys, textwrap

def split_blocks(text):
    """Yield (kind, text) with kind in {'code','prose'}."""
    out, buf, in_fence = [], [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            if not in_fence:
                out.append(("prose", "\n".join(buf))); buf = [line]; in_fence = True
            else:
                buf.append(line); out.append(("code", "\n".join(buf))); buf = []; in_fence = False
            continue
        buf.append(line)
    out.append(("code" if in_fence else "prose", "\n".join(buf)))
    return out

SKIP_START = ("#", ":", "|", "{", "<", "---", "!", "> ")

def unwrap(block):
    paras = block.split("\n\n")
    res = []
    for p in paras:
        lines = p.split("\n")
        if not p.strip():
            res.append(p); continue
        first = lines[0].lstrip()
        if first.startswith(SKIP_START):
            res.append(p); continue
        if first.startswith("- "):
            # bullet list: join continuation lines into each bullet
            bullets, cur = [], []
            for ln in lines:
                if ln.lstrip().startswith("- "):
                    if cur: bullets.append(" ".join(x.strip() for x in cur))
                    cur = [ln]
                else:
                
```

## [77]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cp pc_package/PCR-007_cex.DRAFT.qmd $SC/backup.qmd && uv run python -c "
import sys; sys.path.insert(0,'$SC')
from reflow import process
process('pc_package/PCR-007_cex.DRAFT.qmd', [])
" && diff <(sed 's/[[:space:]]\+/ /g' $SC/backup.qmd | tr -d '\n') <(sed 's/[[:space:]]\+/ /g' pc_package/PCR-007_cex.DRAFT.qmd | tr -d '\n') && echo "CONTENT IDENTICAL" ; uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd 2>&1 | head -6
```

## [79]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cp $SC/backup.qmd pc_package/PCR-007_cex.DRAFT.qmd && python3 - <<'PYEOF'
import re
p = "/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad/reflow.py"
s = open(p).read()
old = """    # put code blocks back
    parts = joined.split("\\n")"""
new = """    # protect inline expressions from being wrapped across lines
    exprs = []
    def _stash(m):
        exprs.append(m.group(0))
        return "\\x01E%dZ\\x01" % (len(exprs) - 1)
    joined = re.sub(r"`\\{python\\}[^`]*`", _stash, joined)
    # put code blocks back
    parts = joined.split("\\n")"""
assert old in s
s = s.replace(old, new)
old2 = """    final = "\\n".join(rewrap(b) if k == "prose" else b for k, b in final_blocks)
    open(path, "w", encoding="utf-8").write(final)"""
new2 = """    final = "\\n".join(rewrap(b) if k == "prose" else b for k, b in final_blocks)
    final = re.sub(r"\\x01E(\\d+)Z\\x01", lambda m: exprs[int(m.group(1))], final)
    open(path, "w", encoding="utf-8").write(final)"""
assert old2 in s
s = s.replace(old2, new2)
open(p, "w").write(s)
print("patched")
PYEOF
uv run python -c "
import sys; sys.path.insert(0,'$SC')
from reflow import process
process('pc_package/PCR-007_cex.DRAFT.qmd', [])
"
uv run python -c "
a=open('$SC/backup.qmd').read().split()
b=open('pc_package/PCR-007_cex.DRAFT.qmd').read().split()
print('same tokens:', a==
```

## [80]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && python3 - <<'PYEOF'
p = "/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad/reflow.py"
s = open(p).read()
old = """    missing = []
    for old, new in edits:
        if old not in joined:
            missing.append(old[:80])
        joined = joined.replace(old, new, 1)"""
new = """    EXPR = r"(`\\{python\\}[^`]*`)"
    missing = []
    for old, new in edits:
        if "@@" in old:
            pat = re.escape(old).replace(re.escape("@@"), EXPR)
            m = re.search(pat, joined)
            if not m:
                missing.append(old[:80]); continue
            out = new
            for i, g in enumerate(m.groups(), 1):
                out = out.replace("@@%d" % i, g)
            joined = joined[:m.start()] + out + joined[m.end():]
        else:
            if old not in joined:
                missing.append(old[:80]); continue
            joined = joined.replace(old, new, 1)"""
assert old in s
s = s.replace(old, new)
open(p, "w").write(s)
print("patched")
PYEOF
```

## [81]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits1.py <<'PYEOF'
EDITS = [
# ---------- executive summary ----------
("The antibody binds below its isoelectric point, the column is washed at a controlled conductivity, and the product is eluted by a pH step and collected to a set optical density on the descending edge of the elution peak.",
 "The antibody binds below its isoelectric point and the column is washed at a controlled conductivity. The product is then eluted by a pH step and collected to a set optical density on the descending edge of the elution peak."),
("Aggregate carries more positive charge than monomer, binds more strongly and elutes late, so the aggregate content of the pool depends on how well the two species are resolved and on where the pool is stopped.",
 "Aggregate carries more positive charge than monomer, binds more strongly and elutes late. Therefore, the aggregate content of the pool depends on how well the two species are resolved and on where the pool is stopped."),
("The tightest capability of the drug substance as a whole is @@, and it belongs to a viral clearance attribute that other steps set.",
 "The tightest capability of the drug substance as a whole is @@1. That capability belongs to a viral clearance attribute which other steps set."),
# ---------- introduction ----------
("The load and the wash are held at a defined conductivity, the product is eluted by a step c
```

## [82]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits2.py <<'PYEOF'
EDITS = [
# ---------- study design ----------
("Protein load was studied from @@ to @@ g/L resin against a normal operating range of @@ to @@ g/L resin, and the other three multivariate factors were widened in the same proportion.",
 "Protein load was studied from @@1 to @@2 g/L resin against a normal operating range of @@3 to @@4 g/L resin. The other three multivariate factors were widened in the same proportion."),
("The load buffer and the wash buffer are the same buffer, so its conductivity is one parameter of the step, and it is called the wash conductivity in the text below.",
 "The load buffer and the wash buffer are the same buffer. Its conductivity is one parameter of the step. The text below calls it the wash conductivity."),
("Axial points at the faces rather than beyond them keep every run inside the characterization range, so no prediction from the model requires a setting the study did not visit.",
 "Axial points at the faces rather than beyond them keep every run inside the characterization range. No prediction from the model therefore requires a setting the study did not visit."),
("Flow rate sets the residence time during elution and therefore the sharpness of the elution peak, but over this range and at the particle size of the resin the change in resolution is small, and the assessment found no effect on pool aggrega
```

## [83]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits3.py <<'PYEOF'
EDITS = [
# ---------- design space ----------
("Protein load appears in both boundaries, with opposite partners, and it is the parameter that carries the operating region.",
 "Protein load appears in both boundaries, with opposite partners. It is the parameter that carries the operating region."),
("The normal operating ranges in @tbl-params are the ranges the process will be operated within at commercial scale, and they lie inside the characterized ranges on every parameter.",
 "The normal operating ranges in @tbl-params are the ranges the process will be operated within at commercial scale. They lie inside the characterized ranges on every parameter."),
("The normal operating ranges are not entirely inside the design space, and the gap is reported here rather than left to be inferred.",
 "The normal operating ranges are not entirely inside the design space. The gap is reported here and is not left to be inferred."),
("The aggregate criterion sits an assurance factor of @@ below the drug substance criterion of @@ % HMW, so a pool predicted at @@ % HMW is above an internal control limit and is not a batch predicted to fail specification.",
 "The aggregate criterion sits an assurance factor of @@1 below the drug substance criterion of @@2 % HMW. A pool predicted at @@3 % HMW is therefore above an internal control limit. It is not a batc
```

## [84]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits4.py <<'PYEOF'
EDITS = [
# ---------- control strategy ----------
("The routine target for load is therefore the set-point rather than the upper part of the range, and a batch executed above @@ g/L resin is assessed against the pool aggregate result before the material is released to the next step.",
 "The routine target for load is therefore the set-point and not the upper part of the range. A batch executed above @@1 g/L resin is assessed against the pool aggregate result before the material is released to the next step."),
("Both limits are derived in §2.2 and both carry an assurance factor below the point at which the drug substance would be at risk, so a result above either one triggers an assessment of the batch and not a rejection of it.",
 "Both limits are derived in §2.2 and both carry an assurance factor below the point at which the drug substance would be at risk. A result above either one triggers an assessment of the batch and not a rejection of it."),
("The characterization in this report was executed on a column within those criteria, and the operating ranges are valid for a column that meets them.",
 "The characterization in this report was executed on a column within those criteria. The operating ranges are valid for a column that meets them."),
("The load is the neutralized pool of the low-pH viral inactivation step, and the aggregat
```

## [85]
```
uv run python - <<'PYEOF'
import sys
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
s = cs.sentences(t)
short = [i for i,x in enumerate(s) if len(x.split()) < 15]
print("sentences", len(s), "short", len(short))
for i in short:
    prev = s[i-1] if i else ""
    print(f"--- [{i}] prev({len(prev.split())}w): {prev[:110]}")
    print(f"    cur({len(s[i].split())}w): {s[i]}")
PYEOF
```

## [86]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && uv run python - <<'PYEOF' > $SC/shorts.txt
import sys
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
s = cs.sentences(t)
for i,x in enumerate(s):
    print(f"[{i}|{len(x.split())}] {x}")
PYEOF
sed -n '1,120p' $SC/shorts.txt
```

## [87]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '120,300p' $SC/shorts.txt
```

## [88]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '300,540p' $SC/shorts.txt
```

## [89]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits5.py <<'PYEOF'
EDITS = [
("per coded coded unit", "per coded unit"),
("the same three surfaces over protein load and load and wash conductivity, with elution buffer pH",
 "the same three surfaces over protein load and wash conductivity, with elution buffer pH"),
# --- exec summary / introduction ---
("It is operated in bind and elute mode on a strong cation exchange resin. The antibody binds below its isoelectric point and the column is washed at a controlled conductivity.",
 "It is operated in bind and elute mode on a strong cation exchange resin, in which the antibody binds below its isoelectric point and the column is washed at a controlled conductivity."),
("Aggregate carries more positive charge than monomer, binds more strongly and elutes late. Therefore, the aggregate content of the pool depends on how well the two species are resolved and on where the pool is stopped.",
 "Aggregate carries more positive charge than monomer and therefore binds more strongly and elutes late, which makes the aggregate content of the pool depend on how well the two species are resolved and on where the pool is stopped."),
("A two-level full factorial screening design of @@ runs identified the active factors. A face centred central composite design of @@ runs then provided the predictive models for pool aggregate, pool host cell protein and step yield.",
 "A two-le
```

## [90]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits6.py <<'PYEOF'
EDITS = [
# --- study design ---
("The characterization ranges bound the knowledge space of the step. Protein load was studied from @@ to @@ g/L resin against a normal operating range of @@ to @@ g/L resin.",
 "The characterization ranges bound the knowledge space of the step, within which protein load was studied from @@1 to @@2 g/L resin against a normal operating range of @@3 to @@4 g/L resin."),
("The load buffer and the wash buffer are the same buffer. Its conductivity is one parameter of the step. The text below calls it the wash conductivity.",
 "The load buffer and the wash buffer are the same buffer, whose conductivity is one parameter of the step and is called the wash conductivity in the text below."),
("The coded design matrix and the measured responses are in Appendix A.",
 "The coded design matrix and the measured responses of the screening design are in Appendix A."),
("Axial points at the faces rather than beyond them keep every run inside the characterization range. No prediction from the model therefore requires a setting the study did not visit.",
 "Axial points at the faces rather than beyond them keep every run inside the characterization range, so no prediction from the model requires a setting the study did not visit."),
("The coded design matrix and the measured responses are in Appendix B.",
 "The coded design m
```

## [91]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits7.py <<'PYEOF'
EDITS = [
# --- design space ---
("The region was evaluated on an even grid of @@ points over the characterized cube. Of those points @@ meet both criteria.",
 "The region was evaluated on an even grid of @@1 points over the characterized cube, of which @@2 meet both criteria."),
("Protein load appears in both boundaries, with opposite partners. It is the parameter that carries the operating region.",
 "Protein load appears in both boundaries, with opposite partners, and is the parameter that carries the operating region."),
("will be operated within at commercial scale. They lie inside the characterized ranges on every parameter.",
 "will be operated within at commercial scale, and lie inside the characterized ranges on every parameter."),
("The normal operating ranges are not entirely inside the design space. The gap is reported here and is not left to be inferred.",
 "The normal operating ranges are not entirely inside the design space, a gap that is reported here and not left to be inferred."),
("Two things bound what that finding means. The in-process criteria are not the drug substance criteria.",
 "Two things bound what that finding means, the first being that the in-process criteria are not the drug substance criteria."),
("the drug substance criterion of @@ % HMW. A pool predicted at @@ % HMW is therefore above an internal cont
```

## [92]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits8.py <<'PYEOF'
EDITS = [
# --- control strategy ---
("The step contributes five elements to the control strategy for commercial manufacture. The first is the set of parameter ranges.",
 "The step contributes five elements to the control strategy for commercial manufacture, the first of which is the set of parameter ranges."),
("The second is in-process monitoring of the two governed responses. Pool aggregate is measured on every batch by AMV-3011 against an in-process limit of @@ % HMW, and pool host cell protein by AMV-3012 against @@ ng/mg.",
 "The second element is in-process monitoring of the two governed responses, in which pool aggregate is measured on every batch by AMV-3011 against an in-process limit of @@1 % HMW and pool host cell protein by AMV-3012 against @@2 ng/mg."),
("The third is the life-cycle control of the column. Resin lot, packing quality and the number of cycles are controlled under SOP-2008,",
 "The third element is the life-cycle control of the column, in which resin lot, packing quality and the number of cycles are controlled under SOP-2008,"),
("The characterization in this report was executed on a column within those criteria. The operating ranges are valid for a column that meets them.",
 "The characterization in this report was executed on a column within those criteria, making the operating ranges valid for a column that
```

## [93]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && grep -n "five elements" pc_package/PCR-007_cex.DRAFT.qmd; uv run python - <<'PYEOF'
import sys
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
s = cs.sentences(t)
print("n", len(s))
for i,x in enumerate(s):
    n=len(x.split())
    if n>=30:
        print(f"[{i}|{n}] {x}")
PYEOF
```

## [94]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && uv run python - <<'PYEOF'
import sys
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
for x in cs.sentences(t):
    if cs.SO_MID.search(x):
        print("SO:", x)
PYEOF
```

## [95]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && cat > $SC/edits9.py <<'PYEOF'
EDITS = [
# --- reduce mid-sentence ", so " to one ---
("Axial points at the faces rather than beyond them keep every run inside the characterization range, so no prediction from the model requires a setting the study did not visit.",
 "Axial points at the faces rather than beyond them keep every run inside the characterization range. No prediction from the model therefore requires a setting the study did not visit."),
("at the stop collect point and in the fraction cut away with the aggregate, so step yield falls.",
 "at the stop collect point and in the fraction cut away with the aggregate, and step yield falls."),
# --- sentence-initial connectives, with splits where useful ---
("Protein load has the largest effect on all three responses, and it governs host cell protein clearance together with the conductivity of the load and wash buffer and aggregate clearance together with elution buffer pH and elution stop collect.",
 "Protein load has the largest effect on all three responses. In addition, it governs host cell protein clearance together with the conductivity of the load and wash buffer, and aggregate clearance together with elution buffer pH and elution stop collect."),
("At commercial scale the step contributes to four drug substance attributes, and simulation of @@ batches",
 "At commercial scale the step contributes to four d
```

## [98]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && uv run python -c "
import sys; sys.path.insert(0,'$SC')
from reflow import process
process('pc_package/PCR-007_cex.DRAFT.qmd', [
 ('a modular clearance claim (Steps 6, 8 and 9)','a modular clearance claim (low-pH inactivation, anion exchange and virus filtration)'),
 ('the centre point of both designs (coded 0) the','the centre point of both designs (the coded origin) the'),
])
"
uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd 2>&1 | sed -n '4,16p'
```

## [99]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && uv run python - <<'PYEOF' > $SC/final.txt
import sys, re
sys.path.insert(0, "authoring")
import check_style as cs
t = cs.prose_from_qmd("pc_package/PCR-007_cex.DRAFT.qmd")
print(t)
PYEOF
sed -n '1,70p' $SC/final.txt
```

## [100]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '70,230p' $SC/final.txt
```

## [101]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '230,400p' $SC/final.txt
```

## [102]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '400,560p' $SC/final.txt
```

## [103]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && sed -n '560,720p' $SC/final.txt
```

## [104]
```
SC=/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/d00e06fe-89dc-4290-beb0-50c6679c7509/scratchpad && uv run python -c "
import sys; sys.path.insert(0,'$SC')
from reflow import process
process('pc_package/PCR-007_cex.DRAFT.qmd', [
 ('The adjusted and the predicted forms stay close to it, and the predicted form is',
  'The adjusted and the predicted forms stay close to the coefficient of determination, and the predicted form is'),
 ('sit outside the region. Step yield carries no proven acceptable range at all,',
  'sit outside the region. The second is that each range stops at the edge of the characterization range, and a row that extends across the whole range is a statement about the range studied and not an unbounded one. Step yield carries no proven acceptable range at all,'),
 ('The root cause was a drift of the chamber controller set-point.',
  'The root cause was a drift of the chamber controller.'),
 ('Aggregate rather than host cell protein bounds this step, which has a consequence for the control strategy.',
  'Aggregate rather than host cell protein bounds this step, and that has a consequence for the control strategy.'),
])
"
uv run python authoring/check_style.py --review pc_package/PCR-007_cex.DRAFT.qmd 2>&1 | tail -12
```

