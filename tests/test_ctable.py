"""Complex tables (Rev 2.0): merged cells reach the DOCX, and every row grounds.

The fixture re-creates the owner's two reference tables
(~/Nextcloud/Datasets/doctool/results/2026-09-30-checkpoint-2/messy/messy.tex) with CTable.
The render test needs Quarto and a LaTeX engine; it is skipped without them.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import zipfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(ROOT, "tests", "fixtures")
sys.path.insert(0, os.path.join(ROOT, "pc_package"))

from ctable import C, CTable  # noqa: E402
from check_grounding import docx_text, normalize  # noqa: E402


def _fixture_tables():
    src = open(os.path.join(FIX, "ctable_messy.qmd")).read()
    code = re.search(r"```\{python\}\n(import sys.*?)```", src, re.S).group(1)
    code = code.replace('os.path.abspath("../../pc_package")', repr(os.path.join(ROOT, "pc_package")))
    g: dict = {}
    exec(code, g)
    return g["T1"], g["T2"]


def test_row_linearization_without_rendering():
    t1, t2 = _fixture_tables()
    assert t1.rows()[1] == "| 25 °C | 99.1 | 97.2 | 95.8"
    assert t2.rows()[2] == "| Dissolved oxygen | % | 40 | not applicable"
    assert t2.rows()[4] == "| | | 12 c) | 0 | 24"
    assert t2.header_rows() == ["Step | Parameter | Unit | Set point | Acceptable range",
                                "| | | | Low | High"]


def test_marker_before_punctuation_reads_as_docx_does():
    t = CTable(header=[["a", "b"]], body=[["x", "SEC^a)^, nrCE-SDS^b)^"]], caption="c", label="tbl-p")
    assert t.rows() == ["x | SEC a) , nrCE-SDS b)"]


def test_ragged_row_is_an_error():
    with pytest.raises(ValueError):
        CTable(header=[["a", "b"]], body=[[C("x", rs=2), "y"], ["z", "extra"]],
               caption="c", label="tbl-x")


def test_latex_twin_has_spans():
    t1, t2 = _fixture_tables()
    assert r"\multirow{3}{*}{A-02}" in t1.latex()
    assert r"\multicolumn{2}{c}{not applicable}" in t2.latex()
    assert r"\textsuperscript{c)}" in t2.latex()
    assert t2.latex().count(r"\midrule") == 2      # header rule + one group rule


@pytest.mark.skipif(shutil.which("quarto") is None, reason="needs quarto")
def test_render_docx_merges_and_grounds(tmp_path):
    work = tmp_path / "fixtures"
    shutil.copytree(FIX, work)
    # the fixture's relative paths point two levels up, at pc_package/
    os.symlink(os.path.join(ROOT, "pc_package"), tmp_path.parent / "pc_package") \
        if not (tmp_path.parent / "pc_package").exists() else None
    r = subprocess.run(["quarto", "render", "ctable_messy.qmd", "--to", "docx"], cwd=work,
                       capture_output=True, text=True,
                       env={**os.environ, "PATH": os.path.join(ROOT, ".venv", "bin") + os.pathsep + os.environ["PATH"]})
    assert r.returncode == 0, r.stderr[-2000:]
    docx = str(work / "ctable_messy.docx")
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode()
    assert xml.count("w:gridSpan") >= 3 and xml.count("w:vMerge") >= 8
    text = docx_text(docx)
    t1, t2 = _fixture_tables()
    for t in (t1, t2):
        for row in t.header_rows() + t.rows() + [t.notes_text()]:
            assert normalize(row) in text, row


def test_line_break_in_a_cell():
    t = CTable(header=[["A", "B"]], body=[["x\ny", "z"]], caption="c.", label="tbl-lb",
               align=["P{2cm}", "l"])
    assert r"x\newline y" in t.latex()
    assert "x<br>y" in t.html()
    assert t.rows() == ["x y | z"]          # the DOCX line break reads as a space


def test_landscape_wraps_only_the_pdf_twin():
    t = CTable(header=[["A"]], body=[["x"]], caption="c.", label="tbl-ls", landscape=True)
    out = t.render()
    assert out.index(r"\begin{landscape}") < out.index("::: {#tbl-ls}") < out.index(r"\end{landscape}")
    assert out.count('when-format="pdf"') == 3 and out.count('when-format="docx"') == 1


def test_cross_reference_in_a_cell_or_note_is_refused():
    """A table cell or note is raw HTML/LaTeX; Quarto would print "@sec-x" literally."""
    import pytest
    from ctable import CTable
    with pytest.raises(ValueError):
        CTable(header=[["A"]], body=[["see @sec-results"]], caption="x", label="tbl-x")
    with pytest.raises(ValueError):
        CTable(header=[["A"]], body=[["1"]], caption="x", label="tbl-x", notes=[("", "As in @tbl-y.")])
    CTable(header=[["A"]], body=[["1"]], caption="As in @tbl-y.", label="tbl-x")
