"""Complex tables: merged cells, two-level headers, footnote markers and footnote rows.

Real study reports are full of these and a flat ``df.to_markdown()`` table can show none of them.
One :class:`CTable` spec renders to two twins inside one Quarto cross-reference div:

* an **HTML table** for DOCX. Quarto parses it into a pandoc table, and the DOCX writer emits real
  merged cells (``w:gridSpan`` across, ``w:vMerge`` down);
* a **raw LaTeX table** for PDF (``booktabs`` + ``multirow``, or one of the ruled styles below).
  Pandoc's own LaTeX writer collapses spanned tables (tested 2026-10-08), so the PDF twin is
  written here.

Both sit in ``::: {#tbl-x}`` with the caption as its last paragraph, so ``@tbl-x`` resolves in
both formats.

Table rules
-----------
Three styles of rules, for the PDF twin only (the HTML twin, and so the DOCX text that the
grounding check reads, is the same in all three):

* ``booktabs`` (the default): top, header and bottom rules, a ``\\cmidrule`` under a header cell
  that spans columns, and a ``\\midrule`` before each group of a table whose first column merges;
* ``rows``: the same top, header and bottom rules, and a thin rule between any two rows, header
  rows included (booktabs' group rule where a group opens). Where a row span continues into the
  next row the rule is cut into ``\\cline`` (``\\cmidrule`` in the header) segments, so it never
  runs through a merged cell, and it runs along the lower border of the merged cell where the span
  ends;
* ``grid``: every cell ruled (``|l|l|`` and a rule under every row), the horizontal rules cut the
  same way and no vertical rule through a cell that spans columns.

A table sets its own style (``CTable(style="grid")``). A whole rendering pass can override every
table with the environment variable ``PC_TABLE_RULES`` (``rows`` or ``grid``; unset or
``booktabs`` keeps each table's own style, today's layout). Quarto's Python kernel inherits the
environment of ``quarto render``, so the variable is read when :meth:`CTable.latex` runs.
``render_variant.py`` (``make corpus-variant RULES=rows``) renders a whole corpus this way, with
the same rules for the plain pipe tables (``table_rules.lua``) and in the DOCX (a reference
document derived from ``reference.docx``); see ``TASKS.md``.

Cells
-----
A cell is a string or ``C(text, rs=1, cs=1, align=None)``. As in HTML, a position covered by a
row span from above is **omitted** from the later row. Write a footnote marker as ``^a)^``;
it renders as a superscript in both formats.

Grounding
---------
:meth:`CTable.rows` returns each row exactly as ``check_grounding.docx_text`` reads it, so an
annex quote can anchor on a merged row. In the DOCX a row-spanned cell leaves an empty
continuation cell in each later row, and a column-spanned cell is one cell. A marker is its own
run, so ``SEC^a)^`` reads as ``SEC a)``.
"""
from __future__ import annotations

import html
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple, Union

CELL_SEP = " | "
_MARK = re.compile(r"\^([^^]+)\^")
_XREF = re.compile(r"@(?:sec|tbl|fig|eq|apx)-[\w-]+")

#: the styles of table rules (see the module docstring)
STYLES = ("booktabs", "rows", "grid")
#: the environment variable that sets the rules of every table in a rendering pass
RULES_ENV = "PC_TABLE_RULES"


def table_rules() -> str:
    """The rules of this rendering pass, from ``PC_TABLE_RULES``: "booktabs" when it is unset or
    "booktabs" (each table keeps its own style), else "rows" or "grid", which override every
    table. Read on each call, so a test can set the variable."""
    v = os.environ.get(RULES_ENV, "").strip().lower()
    if v in ("", "booktabs"):
        return "booktabs"
    if v not in STYLES:
        raise ValueError(f"{RULES_ENV}={v!r}: use one of {', '.join(STYLES)}")
    return v


@dataclass
class C:
    """One table cell. ``rs``/``cs`` are the row and column span."""
    text: object = ""
    rs: int = 1
    cs: int = 1
    align: Optional[str] = None


Cell = Union[str, int, float, C]


def _c(x: Cell) -> C:
    return x if isinstance(x, C) else C(x)


def _s(x) -> str:
    return "" if x is None else str(x)


# -- text conversion ----------------------------------------------------------------------
_LATEX_ESC = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
              "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}"}


def _latex(text: str) -> str:
    """A "\\n" in a cell is a line break (``\\newline``, so the column must wrap: ``P{…}``)."""
    parts = _MARK.split(_s(text))
    out = []
    for i, p in enumerate(parts):
        esc = "".join(_LATEX_ESC.get(ch, ch) for ch in p).replace("\n", r"\newline ")
        out.append(r"\textsuperscript{" + esc + "}" if i % 2 else esc)
    return "".join(out)


def _html(text: str) -> str:
    parts = _MARK.split(_s(text))
    return "".join(f"<sup>{html.escape(p)}</sup>" if i % 2 else html.escape(p).replace("\n", "<br>")
                   for i, p in enumerate(parts))


def _plain(text: str) -> str:
    """The text as the grounding check reads it from the DOCX: a marker is its own run, so the
    tag boundaries on BOTH sides of it read as a space ("SEC a) , nrCE-SDS b)")."""
    return re.sub(r"\s+", " ", _MARK.sub(r" \1 ", _s(text))).strip()


#: characters per centimetre of DejaVu Serif at each table size, measured on rendered tables
#: (INV-001 Tables 4.4 and 6.1): a low value, so that the lines a merged text needs are not
#: underestimated, and a high value, so that the lines a row offers are not overestimated
_CPC_LO = {"tiny": 7.4, "scriptsize": 6.3, "footnotesize": 5.4, "small": 4.9, "normalsize": 4.4}
_CPC_HI = {"tiny": 9.0, "scriptsize": 7.7, "footnotesize": 6.6, "small": 6.0, "normalsize": 5.4}


def _width_cm(spec: str) -> Optional[float]:
    """The width of a wrapping column (``p{3.4cm}``), or None for a column that does not wrap."""
    m = re.search(r"p\{([\d.]+)(cm|mm|in|pt)\}", spec)
    if not m:
        return None
    return float(m.group(1)) * {"cm": 1.0, "mm": 0.1, "in": 2.54, "pt": 0.03515}[m.group(2)]


def _lines_needed(text, width_cm: Optional[float], cpc: float) -> int:
    """How many lines a cell's text takes: its explicit line breaks, and in a wrapping column the
    lines a greedy word wrap at the column width gives."""
    n = 0
    for part in _MARK.sub("", _s(text)).split("\n"):       # a superscript marker takes no line
        if width_cm is None:
            n += 1
            continue
        cap, cur, k = max(1, int(width_cm * cpc)), 0, 1
        for w in part.split():
            if cur == 0:
                cur = len(w)
            elif cur + 1 + len(w) <= cap:
                cur += 1 + len(w)
            else:
                k, cur = k + 1, len(w)
            while cur > cap:
                k, cur = k + 1, cur - cap
        n += k
    return n


def _note(marker: str, text: str) -> str:
    """A footnote: its superscript marker, then the text. An empty marker is a plain note."""
    return f"^{marker}^ {text}" if marker else text


# -- the table ----------------------------------------------------------------------------
@dataclass
class CTable:
    header: List[List[Cell]]
    body: List[List[Cell]]
    caption: str
    label: str                                   # "tbl-..." (without '#')
    align: Optional[str] = None                  # LaTeX column spec letters, e.g. "llrrr"
    notes: Sequence[Tuple[str, str]] = ()        # (marker, text), e.g. ("a)", "Retained samples.")
    notes_per_row: bool = False                  # one footnote row per note (else one row)
    style: str = "booktabs"                      # "booktabs", "rows" or "grid" (PC_TABLE_RULES overrides)
    group_rule: bool = True                      # a rule before each body row that opens a group
    size: str = "small"                          # LaTeX size command for the table body
    resize: bool = True                          # shrink to \linewidth if wider (never enlarges)
    landscape: bool = False                      # PDF: the table on a landscape page of its own
    ncols: int = field(init=False, default=0)

    def __post_init__(self):
        self.header = [[_c(x) for x in r] for r in self.header]
        self.body = [[_c(x) for x in r] for r in self.body]
        # cells and notes are raw HTML/LaTeX, so Quarto never resolves a cross-reference in them
        # and "@sec-x" would print literally. Name the section in words; the caption may refer.
        for t in [c.text for r in self.header + self.body for c in r] + [n[1] for n in self.notes]:
            if _XREF.search(_s(t)):
                raise ValueError(f"{self.label}: a cross-reference cannot resolve inside a table "
                                 f"cell or note ({_XREF.search(_s(t)).group(0)!r}); name it in words")
        self._relabel_notes()
        self.ncols = sum(c.cs for c in self.header[0])
        if not self.label.startswith("tbl-"):
            raise ValueError("label must start with 'tbl-'")
        if self.style not in STYLES:
            raise ValueError(f"{self.label}: style {self.style!r} is not one of {', '.join(STYLES)}")
        self._grid(self.header)
        self._grid(self.body)

    def _relabel_notes(self):
        """Letter footnotes a), b), c) … in the order the table first uses them, and drop a lettered
        note the table never uses. A builder may keep a fixed lettering in its code; the reader
        never sees "e)" without a "d)". Markers that are not a single letter (R1, c1) and notes with
        no marker are left as they are."""
        cells = [c for r in self.header + self.body for c in r]
        order = []
        for c in cells:
            for m in _MARK.findall(_s(c.text)):
                if re.fullmatch(r"[a-z]\)", m) and m not in order:
                    order.append(m)
        if not order:
            return
        new = {m: f"{chr(ord('a') + i)})" for i, m in enumerate(order)}
        rep = lambda t: _MARK.sub(lambda mm: "^" + new.get(mm.group(1), mm.group(1)) + "^", _s(t))
        for c in cells:
            c.text = rep(c.text)
        notes = [(new[m], t) for m, t in self.notes if m in new]
        notes.sort(key=lambda n: n[0])
        keep = [(m, t) for m, t in self.notes if not re.fullmatch(r"[a-z]\)", m or "")]
        self.notes = notes + keep

    def marker_for(self, text: str) -> str:
        """The marker of the note whose text contains ``text`` ("a)"), so prose can cite a note
        without typing a letter that relabelling may change."""
        for m, t in self.notes:
            if text in t:
                return m
        raise KeyError(f"{self.label}: no note contains {text!r}")

    # -- occupancy: which (row, col) a span covers ----------------------------------------
    def _grid(self, rows):
        """List per row of (col, cell) for cells that START in that row, and the set of
        positions covered by a span from above. Raises if a row does not fill the width."""
        covered = set()
        placed = []
        for r, row in enumerate(rows):
            col, cells = 0, []
            it = iter(row)
            while col < self.ncols:
                if (r, col) in covered:
                    col += 1
                    continue
                try:
                    c = next(it)
                except StopIteration:
                    raise ValueError(f"{self.label}: row {r} ends at column {col} of {self.ncols}")
                cells.append((col, c))
                for dr in range(c.rs):
                    for dc in range(c.cs):
                        if dr or dc:
                            covered.add((r + dr, col + dc))
                col += c.cs
            if next(it, None) is not None:
                raise ValueError(f"{self.label}: row {r} has more cells than {self.ncols} columns")
            placed.append(cells)
        return placed, covered

    # -- DOCX twin --------------------------------------------------------------------------
    def _html_rows(self, rows, tag):
        out = []
        for row in rows:
            tds = []
            for c in row:
                attrs = (f' rowspan="{c.rs}"' if c.rs > 1 else "") + (f' colspan="{c.cs}"' if c.cs > 1 else "")
                if c.align:
                    attrs += f' style="text-align: {dict(l="left", c="center", r="right").get(c.align, c.align)}"'
                tds.append(f"<{tag}{attrs}>{_html(c.text)}</{tag}>")
            out.append("<tr>" + "".join(tds) + "</tr>")
        return "\n".join(out)

    def html(self) -> str:
        foot = ""
        if self.notes:
            notes = [[C(_note(m, t), cs=self.ncols)] for m, t in self.notes] if self.notes_per_row \
                else [[C(" ".join(_note(m, t) for m, t in self.notes), cs=self.ncols)]]
            foot = "<tfoot>\n" + self._html_rows(notes, "td") + "\n</tfoot>\n"
        return ("<table>\n<thead>\n" + self._html_rows(self.header, "th") + "\n</thead>\n<tbody>\n"
                + self._html_rows(self.body, "td") + "\n</tbody>\n" + foot + "</table>")

    # -- PDF twin ---------------------------------------------------------------------------
    def _style(self) -> str:
        """The style the PDF twin is set in: the table's own, unless ``PC_TABLE_RULES`` sets the
        rules of the whole pass."""
        rules = table_rules()
        return self.style if rules == "booktabs" else rules

    def _latex_rows(self, rows, rule_groups, style="booktabs", rule_rows=False):
        """The LaTeX lines of ``rows`` (the header or the body). ``rule_rows`` (the body in the rows
        style): a rule under every row but the last, cut around a row span that continues."""
        placed, covered = self._grid(rows)
        origin = self._origins(placed)
        down = self._spanned_down(origin)
        aligns = self._aligns()
        lines = []
        grid = style == "grid"
        ruled = style == "rows"
        # a table is grouped when its first column has a row span somewhere
        grouped = any(c.rs > 1 for cells in placed for col, c in cells if col == 0)
        # the lines each row takes, from its own cells, so that a merged cell whose text needs more
        # lines than the rows it spans can hold is set in the first row of the span (which then
        # grows) instead of in a \multirow that would run through the rule below it
        lo, hi = _CPC_LO.get(self.size, _CPC_LO["small"]), _CPC_HI.get(self.size, _CPC_HI["small"])

        def _w(col, c):
            return _width_cm(aligns[col]) if ("p{" in aligns[col] and c.cs == 1) else None
        row_lines = [max([_lines_needed(c.text, _w(col, c), hi) for col, c in cells if c.rs == 1] or [1])
                     for cells in placed]
        for r, cells in enumerate(placed):
            starts = dict(cells)
            # the grid style already rules every row, and the rows style sets the group rule under
            # the row before, so only booktabs needs a group rule here
            if rule_groups and grouped and not grid and not ruled and r > 0 and (r, 0) not in covered:
                lines.append(r"\hline" if grid else r"\midrule")
            parts, col = [], 0
            while col < self.ncols:
                if col in starts:
                    c = starts[col]
                    txt = _latex(c.text)
                    if r"\newline" in txt and ("p{" not in aligns[col] or c.align or c.cs > 1):
                        # a line break in a column that does not wrap (a header, a short label), or
                        # in a cell with its own alignment or spanning columns, which becomes a
                        # non-wrapping \multicolumn below (a \newline there was dropped, and the words
                        # either side ran together: "pH 3.40against", PCP-006 Table 7.1)
                        a_ = c.align or (aligns[col] if len(aligns[col]) == 1 else "l")
                        txt = r"\makecell[" + a_ + "]{" + txt.replace(r"\newline ", r"\\") + "}"
                    if c.rs > 1 and _lines_needed(c.text, _w(col, c), lo) <= sum(row_lines[r:r + c.rs]):
                        # in a wrapping column the merged text must wrap to the column width
                        w = "=" if "p{" in aligns[col] and c.cs == 1 else "*"
                        txt = r"\multirow{" + str(c.rs) + "}{" + w + "}{" + txt + "}"
                    if c.cs > 1 or grid or c.align:
                        a = c.align or ("c" if c.cs > 1 else aligns[col])
                        if grid:
                            a = ("|" if col == 0 else "") + a + "|"
                        txt = r"\multicolumn{" + str(c.cs) + "}{" + a + "}{" + txt + "}"
                    parts.append(txt)
                    col += c.cs
                else:
                    # a position covered by a row span from above. In the grid style the rows below
                    # the first of a cell that also spans columns are one empty cell across those
                    # columns: an empty cell per column drew the vertical rules of the tabular
                    # through the merged cell
                    orow, ocol = origin[(r, col)]
                    width = next(c.cs for cc, c in placed[orow] if cc == ocol) if grid and ocol == col else 1
                    if width > 1:
                        parts.append(r"\multicolumn{" + str(width) + "}{" + ("|" if col == 0 else "")
                                     + "l|}{}")
                    else:
                        parts.append("")
                    col += width
            lines.append(" & ".join(parts) + r" \\")
            if grid:
                # \cline under every column that does not continue a row span into the next row (a
                # cell of the next row that spans columns does not continue anything: the rule runs
                # above all of its columns)
                spans = [cc for cc in range(self.ncols) if (r + 1, cc) not in down]
                lines.append(self._clines(spans) if len(spans) < self.ncols else r"\hline")
            elif ruled and rule_rows and r + 1 < len(placed):
                # a thin rule under the row, cut into segments where a row span continues: it never
                # runs through a merged cell, and it runs along the lower border of one that ends.
                # Where a group opens, booktabs' group rule instead, cut the same way.
                free = [cc for cc in range(self.ncols) if (r + 1, cc) not in down]
                if rule_groups and grouped and (r + 1, 0) not in down:
                    lines.append(r"\midrule" if len(free) == self.ncols else self._cmidrules(free))
                else:
                    lines.append(r"\hline" if len(free) == self.ncols else self._clines(free))
        return lines, placed

    @staticmethod
    def _origins(placed):
        """Each position a span covers -> the (row, col) of the cell the span starts at."""
        origin = {}
        for r, cells in enumerate(placed):
            for col, c in cells:
                for dr in range(c.rs):
                    for dc in range(c.cs):
                        if dr or dc:
                            origin[(r + dr, col + dc)] = (r, col)
        return origin

    @staticmethod
    def _spanned_down(origin):
        """The positions covered by a cell that starts in a row above: where a row span continues.
        ``_grid``'s covered set also holds the positions a cell covers to its right in its own row,
        and a rule cut at those left a gap above every cell that spans columns but its first."""
        return {pos for pos, (orow, _) in origin.items() if orow < pos[0]}

    @staticmethod
    def _runs(cols):
        """Consecutive column indices as (first, last) runs: [0, 1, 3] -> [(0, 1), (3, 3)]."""
        out, start = [], None
        for i, c in enumerate(cols):
            if start is None:
                start = c
            if i + 1 == len(cols) or cols[i + 1] != c + 1:
                out.append((start, c))
                start = None
        return out

    @classmethod
    def _clines(cls, cols):
        return " ".join(rf"\cline{{{a + 1}-{b + 1}}}" for a, b in cls._runs(cols))

    @classmethod
    def _cmidrules(cls, cols):
        return " ".join(rf"\cmidrule{{{a + 1}-{b + 1}}}" for a, b in cls._runs(cols))

    def _header_rules(self, placed, r):
        """The rows style: the rule under header row ``r``, along every column that does not
        continue a row span into the next header row. Under a cell that spans columns it is trimmed
        at both ends, as booktabs sets it, so that two groups side by side stay apart."""
        down = self._spanned_down(self._origins(placed))
        free = [cc for cc in range(self.ncols) if (r + 1, cc) not in down]
        groups = [(col, col + c.cs - 1) for col, c in placed[r] if c.cs > 1 and col in free]
        in_group = {cc for a, b in groups for cc in range(a, b + 1)}
        segs = [(a, b, "(lr)") for a, b in groups]
        segs += [(a, b, "") for a, b in self._runs([cc for cc in free if cc not in in_group])]
        return [rf"\cmidrule{t}{{{a + 1}-{b + 1}}}" for a, b, t in sorted(segs)]

    def _aligns(self):
        """Column specs. ``align`` is a string of l/c/r letters, or a list whose entries may also
        be ``"P{2.5cm}"`` (wrapping, ragged right) or ``"R{1.3cm}"`` (wrapping, ragged left)."""
        a = self.align or ("l" * self.ncols)
        out = []
        for tok in (list(a) if isinstance(a, str) else a):
            m = re.fullmatch(r"([PR])\{(.+)\}", tok)
            if m:
                rag = r"\raggedright" if m.group(1) == "P" else r"\raggedleft"
                tok = r">{" + rag + r"\arraybackslash}p{" + m.group(2) + "}"
            out.append(tok)
        return out

    def latex(self) -> str:
        style = self._style()
        grid, ruled = style == "grid", style == "rows"
        spec = "|" + "|".join(self._aligns()) + "|" if grid else "".join(self._aligns())
        L = [r"{\%s" % self.size, r"\setlength{\tabcolsep}{4pt}"]
        if self.resize:
            # shrink to the text width if wider; never enlarge a narrow table
            L.append(r"\begin{adjustbox}{max width=\linewidth}")
        # threeparttable: the notes take the width of the table. A note set as a full-width
        # \multicolumn row would instead widen the LAST column to the length of the note.
        L.append(r"\begin{threeparttable}")
        L.append(r"\begin{tabular}{" + spec + "}")
        L.append(r"\hline" if grid else r"\toprule")
        # header, with \cmidrule under every column-spanning header cell that has a row below it
        # (the rows style: under every header cell that ends above the next header row)
        hplaced, _ = self._grid(self.header)
        hl, _ = self._latex_rows(self.header, rule_groups=False, style=style)
        if not grid:
            out = []
            for r, line in enumerate(hl):
                out.append(line)
                if r + 1 < len(self.header):
                    if ruled:
                        mids = self._header_rules(hplaced, r)
                    else:
                        mids = [rf"\cmidrule(lr){{{col + 1}-{col + c.cs}}}" for col, c in hplaced[r] if c.cs > 1]
                    if mids:
                        out.append(" ".join(mids))
            hl = out
        L += hl
        L.append("" if grid else r"\midrule")
        bl, _ = self._latex_rows(self.body, rule_groups=self.group_rule, style=style, rule_rows=ruled)
        L += bl
        if not grid:
            L.append(r"\bottomrule")
        L.append(r"\end{tabular}")
        if self.notes:
            L.append(r"\begin{tablenotes}[flushleft]\footnotesize")
            if self.notes_per_row:
                L += [r"\item[" + _latex(m) + "] " + _latex(t) for m, t in self.notes]
            else:
                L.append(r"\item[] " + _latex(" ".join(_note(m, t) for m, t in self.notes)))
            L.append(r"\end{tablenotes}")
        L.append(r"\end{threeparttable}")
        if self.resize:
            L.append(r"\end{adjustbox}")
        L.append("}")
        return "\n".join(x for x in L if x != "")

    # -- the Quarto block -------------------------------------------------------------------
    def render(self) -> str:
        if self.landscape:
            # outside the cross-reference div, so the caption turns with the table
            on = "::: {.content-visible when-format=\"pdf\"}\n```{=latex}\n\\begin{landscape}\n```\n:::\n\n"
            off = "\n::: {.content-visible when-format=\"pdf\"}\n```{=latex}\n\\end{landscape}\n```\n:::\n"
            return on + self._block() + off
        return self._block()

    def _block(self) -> str:
        return (f"::: {{#{self.label}}}\n\n"
                "::: {.content-visible when-format=\"docx\"}\n```{=html}\n" + self.html() + "\n```\n:::\n\n"
                "::: {.content-visible when-format=\"pdf\"}\n```{=latex}\n" + self.latex() + "\n```\n:::\n\n"
                f"{self.caption}\n\n:::\n")

    def show(self):
        """Print the block. The chunk must carry ``#| output: asis``."""
        print(self.render())

    # -- grounding --------------------------------------------------------------------------
    def _linear(self, rows) -> List[str]:
        placed, _ = self._grid(rows)
        origin = {}                       # covered (row, col) -> (origin row, origin col)
        for r, cells in enumerate(placed):
            for col, c in cells:
                for dr in range(c.rs):
                    for dc in range(c.cs):
                        if dr or dc:
                            origin[(r + dr, col + dc)] = (r, col)
        out = []
        for r, cells in enumerate(placed):
            starts = dict(cells)
            vals, col = [], 0
            while col < self.ncols:
                if col in starts:
                    vals.append(_plain(starts[col].text))
                    col += starts[col].cs
                    continue
                orow, ocol = origin[(r, col)]
                if orow < r and ocol == col:
                    # a row-span continuation is an empty cell of its own in the DOCX (vMerge);
                    # when the origin also spans columns, that one cell carries the gridSpan
                    vals.append("")
                    width = next(c.cs for cc, c in placed[orow] if cc == ocol)
                    col += width
                else:
                    col += 1
            out.append(re.sub(r"\s+", " ", CELL_SEP.join(vals)).strip())
        return out

    def rows(self) -> List[str]:
        """Body rows, each as the grounding check reads it from the DOCX."""
        return self._linear(self.body)

    def header_rows(self) -> List[str]:
        return self._linear(self.header)

    def notes_text(self) -> str:
        """The footnote row(s) as the grounding check reads them."""
        if self.notes_per_row:
            return CELL_SEP.join(_plain(_note(m, t)) for m, t in self.notes)
        return _plain(" ".join(_note(m, t) for m, t in self.notes))
