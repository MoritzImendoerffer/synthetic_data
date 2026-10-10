"""Table rules of the complex tables (owner, 2026-10-10): the default layout is unchanged, and the
two variant styles put a rule between every pair of rows and never through a merged cell.

``booktabs`` is the layout every rendered document had before the switch existed. Its LaTeX is
pinned here verbatim, as the original ``ctable.py`` wrote it for these tables (generated
2026-10-10, before the change). ``rows`` and ``grid`` are checked structurally: between two
consecutive rows the rules must cover exactly the columns in which no row span continues.
"""
from __future__ import annotations

import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))

import ctable  # noqa: E402
from ctable import C, CTable  # noqa: E402


@pytest.fixture(autouse=True)
def _default_pass(monkeypatch):
    monkeypatch.delenv(ctable.RULES_ENV, raising=False)


def _tables():
    # a two-level header (row spans and a column group), a merged first column (groups), a merged
    # last column, a line break in a header cell, a wrapping column, an escaped "&", notes
    t1 = CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Criterion", cs=2), C("Basis\nof the limit", rs=2)],
                ["Low", "High"]],
        body=[[C("Protein A", rs=3), "HCP (ng/mg)", "–", "≤ 10,724", C("carried back^a)^", rs=2)],
              ["Leached Protein A", "–", "≤ 158"],
              ["Fragments", "–", "≤ 2.45", "platform"],
              [C("CEX", rs=2), "Aggregates", "–", "≤ 2.17", "R1"],
              ["HCP & DNA", "–", "≤ 100", "R2"]],
        caption="A test table.", label="tbl-test-one",
        align=["l", "P{2.6cm}", "r", "r", "l"],
        notes=[("a)", "A note."), ("", "A plain note.")], notes_per_row=True)
    # a cell that spans rows and columns, in a table that sets the grid style itself
    t2 = CTable(
        header=[["Run", "Type", "A", "B", "C"]],
        body=[["1", C("factorial", rs=2), C("no result", rs=2, cs=2), "x"],
              ["2", "y"],
              ["3", "centre", "0", "0", "z"]],
        caption="A second test table.", label="tbl-test-two", style="grid")
    # a three-level header (as doe_results) and a run type merged in the second column
    t3 = CTable(
        header=[[C("Run", rs=3), C("Type", rs=3), C("Factor settings", cs=2), C("Responses", cs=2)],
                ["A", "B", "Titre", "HMW"], ["g/L", "°C", "g/L", "%"]],
        body=[["1", C("factorial", rs=2), "−1", "−1", "2.1", "1.0"],
              ["2", "+1", "−1", "2.3", "1.1"],
              ["3", "centre", "0", "0", "2.2", "1.0"]],
        caption="A third test table.", label="tbl-test-three", size="footnotesize")
    # cells that span columns below the first row, in the header and in the body (as the "not
    # applicable" of iac_derivation): the rule above them runs along all of their columns
    t4 = CTable(
        header=[[C("Attribute", rs=3), C("Downstream", cs=3)],
                [C("Platform", cs=2), C("Verified", rs=2)],
                ["Factor", "Increase"]],
        body=[["Aggregates", "1.40", "0.00", "yes"],
              ["XMuLV", C("not applicable", cs=2), "–"],
              [C("Fragments", rs=2), "1.30", "0.00", "yes"],
              [C("not tested", cs=3)]],
        caption="A fourth test table.", label="tbl-test-four")
    return {"t1": t1, "t2": t2, "t3": t3, "t4": t4}


# -- the default layout, verbatim as the original module wrote it -------------------------------
GOLDEN_T1 = r"""{\small
\setlength{\tabcolsep}{4pt}
\begin{adjustbox}{max width=\linewidth}
\begin{threeparttable}
\begin{tabular}{l>{\raggedright\arraybackslash}p{2.6cm}rrl}
\toprule
\multirow{2}{*}{Step} & \multirow{2}{=}{Attribute} & \multicolumn{2}{c}{Criterion} & \multirow{2}{*}{\makecell[l]{Basis\\of the limit}} \\
\cmidrule(lr){3-4}
 &  & Low & High &  \\
\midrule
\multirow{3}{*}{Protein A} & HCP (ng/mg) & – & ≤ 10,724 & \multirow{2}{*}{carried back\textsuperscript{a)}} \\
 & Leached Protein A & – & ≤ 158 &  \\
 & Fragments & – & ≤ 2.45 & platform \\
\midrule
\multirow{2}{*}{CEX} & Aggregates & – & ≤ 2.17 & R1 \\
 & HCP \& DNA & – & ≤ 100 & R2 \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]\footnotesize
\item[a)] A note.
\item[] A plain note.
\end{tablenotes}
\end{threeparttable}
\end{adjustbox}
}"""

GOLDEN_T3 = r"""{\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{adjustbox}{max width=\linewidth}
\begin{threeparttable}
\begin{tabular}{llllll}
\toprule
\multirow{3}{*}{Run} & \multirow{3}{*}{Type} & \multicolumn{2}{c}{Factor settings} & \multicolumn{2}{c}{Responses} \\
\cmidrule(lr){3-4} \cmidrule(lr){5-6}
 &  & A & B & Titre & HMW \\
 &  & g/L & °C & g/L & \% \\
\midrule
1 & \multirow{2}{*}{factorial} & −1 & −1 & 2.1 & 1.0 \\
2 &  & +1 & −1 & 2.3 & 1.1 \\
3 & centre & 0 & 0 & 2.2 & 1.0 \\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{adjustbox}
}"""

# the grid style a builder may set (hold_stability, pp_cqa_matrix), on a table with no cell that
# spans both rows and columns: unchanged too
GOLDEN_T1_GRID = r"""{\small
\setlength{\tabcolsep}{4pt}
\begin{adjustbox}{max width=\linewidth}
\begin{threeparttable}
\begin{tabular}{|l|>{\raggedright\arraybackslash}p{2.6cm}|r|r|l|}
\hline
\multicolumn{1}{|l|}{\multirow{2}{*}{Step}} & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{\multirow{2}{=}{Attribute}} & \multicolumn{2}{c|}{Criterion} & \multicolumn{1}{l|}{\multirow{2}{*}{\makecell[l]{Basis\\of the limit}}} \\
\cline{3-4}
 &  & \multicolumn{1}{r|}{Low} & \multicolumn{1}{r|}{High} &  \\
\hline
\multicolumn{1}{|l|}{\multirow{3}{*}{Protein A}} & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{HCP (ng/mg)} & \multicolumn{1}{r|}{–} & \multicolumn{1}{r|}{≤ 10,724} & \multicolumn{1}{l|}{\multirow{2}{*}{carried back\textsuperscript{a)}}} \\
\cline{2-4}
 & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{Leached Protein A} & \multicolumn{1}{r|}{–} & \multicolumn{1}{r|}{≤ 158} &  \\
\cline{2-5}
 & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{Fragments} & \multicolumn{1}{r|}{–} & \multicolumn{1}{r|}{≤ 2.45} & \multicolumn{1}{l|}{platform} \\
\hline
\multicolumn{1}{|l|}{\multirow{2}{*}{CEX}} & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{Aggregates} & \multicolumn{1}{r|}{–} & \multicolumn{1}{r|}{≤ 2.17} & \multicolumn{1}{l|}{R1} \\
\cline{2-5}
 & \multicolumn{1}{>{\raggedright\arraybackslash}p{2.6cm}|}{HCP \& DNA} & \multicolumn{1}{r|}{–} & \multicolumn{1}{r|}{≤ 100} & \multicolumn{1}{l|}{R2} \\
\hline
\end{tabular}
\begin{tablenotes}[flushleft]\footnotesize
\item[a)] A note.
\item[] A plain note.
\end{tablenotes}
\end{threeparttable}
\end{adjustbox}
}"""


@pytest.mark.parametrize("env", [None, "booktabs", "BookTabs "])
def test_booktabs_is_the_layout_before_the_switch(monkeypatch, env):
    if env is not None:
        monkeypatch.setenv(ctable.RULES_ENV, env)
    t = _tables()
    assert t["t1"].latex() == GOLDEN_T1
    assert t["t3"].latex() == GOLDEN_T3
    t1 = _tables()["t1"]
    t1.style = "grid"
    assert t1.latex() == GOLDEN_T1_GRID


def test_a_table_keeps_its_own_style_in_the_default_pass():
    t2 = _tables()["t2"]
    assert t2.latex().startswith(r"{\small") and r"\begin{tabular}{|l|l|l|l|l|}" in t2.latex()


@pytest.mark.parametrize("rules", ["rows", "grid"])
def test_the_switch_overrides_every_table(monkeypatch, rules):
    monkeypatch.setenv(ctable.RULES_ENV, rules)
    for name, t in _tables().items():
        spec = re.search(r"\\begin\{tabular\}\{(.*)\}\n", t.latex()).group(1)
        assert ("|" in spec) == (rules == "grid"), name


def test_an_unknown_switch_or_style_is_an_error(monkeypatch):
    monkeypatch.setenv(ctable.RULES_ENV, "dotted")
    with pytest.raises(ValueError):
        _tables()["t1"].latex()
    monkeypatch.delenv(ctable.RULES_ENV)
    with pytest.raises(ValueError):
        CTable(header=[["a"]], body=[["b"]], caption="c", label="tbl-s", style="dotted")


@pytest.mark.parametrize("rules", ["rows", "grid"])
def test_the_rules_change_neither_the_docx_twin_nor_the_grounding_text(monkeypatch, rules):
    before = {k: (t.html(), t.rows(), t.header_rows(), t.notes_text()) for k, t in _tables().items()}
    monkeypatch.setenv(ctable.RULES_ENV, rules)
    after = {k: (t.html(), t.rows(), t.header_rows(), t.notes_text()) for k, t in _tables().items()}
    assert before == after


# -- the variant styles, checked structurally ----------------------------------------------------
_RULE = re.compile(r"\\(hline|midrule|toprule|bottomrule)\b|\\(cline|cmidrule)(?:\([lr]+\))?\{(\d+)-(\d+)\}")


def _cells(row: str):
    """The cells of one LaTeX row, split at the "&" that are not escaped and not inside braces."""
    out, depth, cur, i = [], 0, "", 0
    while i < len(row):
        ch = row[i]
        if ch == "\\":
            cur += row[i:i + 2]
            i += 2
            continue
        depth += ch == "{"
        depth -= ch == "}"
        if ch == "&" and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
        i += 1
    out.append(cur.strip())
    return out


def _width(cell: str) -> int:
    m = re.match(r"\\multicolumn\{(\d+)\}", cell)
    return int(m.group(1)) if m else 1


def _structure(latex: str, ncols: int):
    """[(row cells, set of columns ruled below the row)] from the tabular of ``latex``."""
    body = latex.split(r"\begin{tabular}", 1)[1].split(r"\end{tabular}", 1)[0]
    lines = [ln.strip() for ln in body.splitlines()[1:] if ln.strip()]
    rows, pending = [], None
    for ln in lines:
        if ln.endswith(r"\\"):
            rows.append([_cells(ln[:-2]), set()])
            continue
        cols = set()
        for m in _RULE.finditer(ln):
            if m.group(1):
                cols |= set(range(ncols))
            else:
                cols |= set(range(int(m.group(3)) - 1, int(m.group(4))))
        assert cols, f"not a row and not a rule: {ln!r}"
        if rows:
            rows[-1][1] |= cols
    return rows


def _continuing(t: CTable):
    """For each boundary below a row (header rows, then body rows): the columns in which a row
    span continues into the next row; None below the last header row and the last body row. A
    cell that spans columns only continues nothing."""
    out = []
    for part in (t.header, t.body):
        placed, _ = t._grid(part)                      # where each cell starts
        down = {(r + dr, col + dc) for r, cells in enumerate(placed) for col, c in cells
                for dr in range(1, c.rs) for dc in range(c.cs)}
        n = len(part)
        out += [{c for c in range(t.ncols) if (r + 1, c) in down} if r + 1 < n else None for r in range(n)]
    return out


@pytest.mark.parametrize("rules", ["rows", "grid"])
@pytest.mark.parametrize("name", ["t1", "t2", "t3", "t4"])
def test_a_rule_between_every_pair_of_rows_and_never_through_a_merged_cell(monkeypatch, rules, name):
    monkeypatch.setenv(ctable.RULES_ENV, rules)
    t = _tables()[name]
    rows = _structure(t.latex(), t.ncols)
    assert len(rows) == len(t.header) + len(t.body)
    for i, ((cells, ruled), cont) in enumerate(zip(rows, _continuing(t))):
        # every row fills the width of the table
        assert sum(_width(c) for c in cells) == t.ncols, (name, i, cells)
        if cont is None:          # below the header, and below the last row: a full rule
            assert ruled == set(range(t.ncols)), (name, i, ruled)
        else:                     # a rule along every column but those a row span continues in
            assert ruled == set(range(t.ncols)) - cont, (name, i, ruled, cont)


def test_rows_style_keeps_the_booktabs_frame_and_group_rules(monkeypatch):
    monkeypatch.setenv(ctable.RULES_ENV, "rows")
    lt = _tables()["t1"].latex()
    assert lt.count(r"\toprule") == 1 and lt.count(r"\bottomrule") == 1
    assert "|" not in re.search(r"\\begin\{tabular\}\{(.*)\}\n", lt).group(1)
    # the header rule below the column group is trimmed, as booktabs sets it
    assert r"\cmidrule(lr){3-4}" in lt
    # header rule + one group rule, and hairlines within the groups, cut around the merged cells
    assert lt.count(r"\midrule") == 2
    assert r"\cline{2-4}" in lt and r"\cline{2-5}" in lt


@pytest.mark.parametrize("rules", ["rows", "grid"])
def test_the_rule_above_a_cell_that_spans_columns_is_whole(monkeypatch, rules):
    """The rule above "not applicable" (two columns) and above "not tested" (three columns) runs
    along every one of their columns; the old grid rule stopped after the first."""
    monkeypatch.setenv(ctable.RULES_ENV, rules)
    t4 = _tables()["t4"]
    rows = _structure(t4.latex(), t4.ncols)
    body = rows[len(t4.header):]
    assert body[0][1] == {0, 1, 2, 3}          # above "not applicable"
    assert body[2][1] == {1, 2, 3}             # above "not tested", beside the merged "Fragments"
    header = rows[:len(t4.header)]
    assert header[0][1] == {1, 2, 3}           # under "Downstream", above "Platform" (two columns)


def test_grid_merges_the_continuation_of_a_cell_across_rows_and_columns(monkeypatch):
    """The second row of a cell that spans two rows and two columns is one empty cell across both
    columns: an empty cell per column drew the vertical rule between them through the merged cell."""
    t2 = _tables()["t2"]                                   # its own style is grid
    rows = _structure(t2.latex(), t2.ncols)
    second = rows[2][0]                                     # header, row 1, row 2
    assert second == [r"\multicolumn{1}{|l|}{2}", "", r"\multicolumn{2}{l|}{}", r"\multicolumn{1}{l|}{y}"]
    # the rule below row 1 runs along columns 1 and 5 only (2 to 4 continue)
    assert rows[1][1] == {0, 4}
