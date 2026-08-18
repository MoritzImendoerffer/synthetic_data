#!/usr/bin/env python3
"""Build the two untracked probe files from the template, the setup code and the shipped text.

    uv run python .claude/work/2026-08-18_03_author-facing-apparatus/build_probe_scaffold.py

Writes, in pc_package/ (so `from _pcpkg import *`, `../outputs/…` and reference.docx resolve):

  PCR-005_protein_a.PROBE.qmd    template + probe-setup.py + two EMPTY subsections under
                                 `# Results` (the agent of TASK-003 writes into them)
  PCR-005_protein_a.EXCERPT.qmd  the same scaffold with the shipped subsections pasted verbatim
                                 (PCR-005_protein_a.qmd lines 747–876), the text the owner
                                 quoted eight sentences from

Both carry the same front matter, the same title block and the same appendix, so their PDFs
differ only in the prose of the two subsections. The appendix exists because the shipped text
cross-references two screening-effect tables (@tbl-eff-hcp, @tbl-eff-yield) that live in the
subsection before the excerpt; without them Quarto prints "?@tbl-eff-hcp", which would mark the
excerpt. The two chunks are copied from the shipped file as code; the probe gets the identical
appendix so the two PDFs stay parallel.

Neither output is tracked. Neither is ever spliced into PCR-005_protein_a.qmd.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))
from _pcpkg import DOC_REGISTRY  # noqa: E402

DOC, UO = "PCR-005", "protein_a"
DOC_CLASS, UO_TITLE, _ = DOC_REGISTRY[DOC]
SHIPPED = os.path.join(ROOT, "pc_package", f"{DOC}_{UO}.qmd")
TEMPLATE = os.path.join(ROOT, "authoring", "template.qmd")
SETUP = os.path.join(HERE, "probe-setup.py")
EXCERPT_LINES = (747, 876)          # `## Response-surface models` … the line before `# Design space`

APPENDIX = '''
{{< pagebreak >}}

# Appendix — screening effect tables referenced in the text {.unnumbered}

```{python}
#| output: asis
show(D.screening_effects_df(UO, "pool_hcp_ng_mg", top=6))
print("\\n: Screening effect estimates for pool host cell protein, the six largest by "
      "magnitude. {#tbl-eff-hcp}\\n")
```

```{python}
#| output: asis
show(D.screening_effects_df(UO, "step_yield", top=6))
print("\\n: Screening effect estimates for step yield, the six largest by magnitude. "
      "{#tbl-eff-yield}\\n")
```
'''

PROBE_BODY = '''# Results

## Response-surface models

<!-- __PROBE_WRITE_HERE__ -->

## Mechanistic interpretation

<!-- __PROBE_WRITE_HERE__ -->
'''


def scaffold(body: str) -> str:
    t = open(TEMPLATE, encoding="utf-8").read()
    t = (t.replace("__DOC_CLASS__", DOC_CLASS).replace("__DOC__", DOC)
          .replace("__UO_KEY__", UO).replace("__UO_TITLE__", UO_TITLE))
    # the template's own comment block, between the front matter and the setup chunk
    t = re.sub(r"<!--\s*=+\s*TEMPLATE — do not author here.*?-->\s*", "", t, flags=re.S)
    # the setup chunk: the template's placeholder body becomes probe-setup.py verbatim
    setup = open(SETUP, encoding="utf-8").read().rstrip("\n")
    t = re.sub(r"```\{python\}\n#\| tags: \[setup\]\n.*?\n```",
               "```{python}\n#| tags: [setup]\n" + setup.replace("\\", "\\\\") + "\n```",
               t, count=1, flags=re.S)
    # no Approvals, no Abbreviations, no References: the probe is two subsections, not a document
    t = re.sub(r"## Approvals \{\.unnumbered\}.*?\{\{< pagebreak >\}\}\s*", "", t, flags=re.S)
    t = re.sub(r"<!-- =+ BODY START.*?BODY END =+ -->", "<!-- BODY -->", t, flags=re.S)
    t = re.sub(r"# References \{\.unnumbered\}\s*::: \{#refs\}\s*:::\s*", "", t, flags=re.S)
    return t.replace("<!-- BODY -->", body.rstrip("\n") + "\n" + APPENDIX)


def main() -> int:
    lines = open(SHIPPED, encoding="utf-8").read().split("\n")
    lo, hi = EXCERPT_LINES
    assert lines[lo - 1].startswith("## Response-surface models"), lines[lo - 1]
    assert lines[hi].startswith("# Design space"), lines[hi]
    excerpt = "\n".join(lines[lo - 1:hi])
    out_probe = os.path.join(ROOT, "pc_package", f"{DOC}_{UO}.PROBE.qmd")
    out_exc = os.path.join(ROOT, "pc_package", f"{DOC}_{UO}.EXCERPT.qmd")
    open(out_probe, "w", encoding="utf-8").write(scaffold(PROBE_BODY))
    open(out_exc, "w", encoding="utf-8").write(scaffold("# Results\n\n" + excerpt + "\n"))
    # prove the excerpt body is the shipped text, byte for byte
    body = open(out_exc, encoding="utf-8").read()
    assert excerpt in body, "excerpt body is not verbatim"
    print(f"wrote {out_probe}\nwrote {out_exc}\nexcerpt lines {lo}-{hi} verbatim: yes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
