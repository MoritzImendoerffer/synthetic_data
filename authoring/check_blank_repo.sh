#!/usr/bin/env bash
# =====================================================================================
# check_blank_repo.sh — prove the one-pass authoring pipeline is independent of the
# first-pass corpus. The existing pc_package/*.qmd are PRIOR KNOWLEDGE (distilled once
# into authoring/), never a runtime input. After distillation, authoring a document may
# depend only on: config -> model -> outputs/, the _pcpkg / doe_report helpers, and the
# authoring/ artifacts.
#
# Two checks:
#   1. STATIC  — no authoring/ file instructs reading a pc_package/*.qmd as an
#                exemplar / source / baseline input.
#   2. FUNCTIONAL — with EVERY pc_package/*.qmd moved aside (the blank-repo condition),
#                build_brief.py + template.qmd + check_render.py + the helpers still
#                produce and gate a grounded document.
#
# Usage:  bash authoring/check_blank_repo.sh [--render]
# Exit 0 iff both checks pass. The moved .qmd files and the probe are always restored.
# =====================================================================================
set -euo pipefail
shopt -s nullglob

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
cd "$ROOT"

RENDER=""
[[ "${1:-}" == "--render" ]] && RENDER="--render"

PROBE="pc_package/_blankrepo_probe.qmd"
STASH="$(mktemp -d)"
fail=0

restore() {
  # move any stashed .qmd back, remove the probe + its render artifacts
  local f
  for f in "$STASH"/*.qmd; do [[ -e "$f" ]] && mv -f "$f" pc_package/; done
  rm -f "$PROBE" "${PROBE%.qmd}.docx"
  rm -rf "$STASH"
}
trap restore EXIT

echo "== 1. STATIC: no authoring/ file reads a pc_package/*.qmd as an input =="
# Flag a read/exemplar/source/baseline verb on the same line as a concrete
# pc_package/<name>.qmd path. Output paths ("-> pc_package/<DOC>.qmd"), the gate's usage
# examples, and "you do NOT need any pc_package/*.qmd" do not match.
if grep -rniE '(read|open|bind|exemplar|source|baseline)[^\n]*pc_package/[A-Za-z0-9_.-]+\.qmd' \
        authoring/ --include='*.md' --include='*.py' --include='*.qmd' --include='*.yaml' \
        | grep -v 'check_blank_repo'; then
  echo "FAIL  an authoring/ file appears to read a pc_package/*.qmd as input (above)"
  fail=1
else
  echo "OK    no first-pass report is used as an authoring input"
fi

echo
echo "== 2. FUNCTIONAL: run the pipeline with every pc_package/*.qmd removed =="
n=0
for f in pc_package/*.qmd; do mv "$f" "$STASH"/; n=$((n+1)); done
echo "   moved $n pc_package/*.qmd aside -> blank-repo condition"
remaining=$(find pc_package -maxdepth 1 -name '*.qmd' | wc -l | tr -d ' ')
echo "   pc_package/*.qmd now present: $remaining (expect 0)"
if [[ "$remaining" != "0" ]]; then
  echo "FAIL  first-pass reports were not removed — the proof would be hollow"
  fail=1
fi

echo "   [a] build_brief.py PCR-003"
uv run python authoring/build_brief.py PCR-003 >/dev/null
test -s authoring/out/PCR-003.brief.md && echo "       OK brief generated"

echo "   [b] instantiate template.qmd -> probe with grounded inline expressions"
uv run python - "$PROBE" <<'PY'
import re, sys
tmpl = open("authoring/template.qmd", encoding="utf-8").read()
# real instantiation replaces the tokens AND deletes the template instruction comment
tmpl = re.sub(r"<!--.*?-->\n?", "", tmpl, count=1, flags=re.DOTALL)
doc = (tmpl
       .replace("__DOC_CLASS__", "Process Characterization Report")
       .replace("__DOC__", "PCR-003")
       .replace("__UO_KEY__", "bioreactor")
       .replace("__UO_TITLE__", "Production Bioreactor (Step 3)"))
# minimal grounded body: exercise both a scalar inline expr and an asis helper table
body = (
    "# Probe {.unnumbered}\n\n"
    "The bioreactor screening design used "
    "`{python} f\"{doe_runs(UO, 'screening')}\"` runs and the step sets "
    "`{python} f\"{len(cqas_for(UO))}\"` CQAs, at a Monte-Carlo capability base of "
    "`{python} f\"{V['n_monte_carlo']:,}\"` batches.\n\n"
    "```{python}\n#| output: asis\nshow(report_params(UO))\n```\n"
)
doc = doc.replace("<!-- ========================= BODY END", body +
                  "<!-- ========================= BODY END")
open(sys.argv[1], "w", encoding="utf-8").write(doc)
print("       OK probe written:", sys.argv[1])
PY

echo "   [c] check_render.py on the probe (blank repo)"
if uv run python authoring/check_render.py "$PROBE" $RENDER; then
  echo "       OK pipeline runs with zero first-pass reports present"
else
  echo "FAIL  pipeline failed under the blank-repo condition"
  fail=1
fi

echo
if [[ "$fail" -eq 0 ]]; then
  echo "PASS  blank-repo independence proven (static + functional)."
else
  echo "FAIL  blank-repo independence NOT proven — see above."
fi
exit "$fail"
