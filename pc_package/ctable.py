"""Complex tables: merged cells, two-level headers, footnote markers and footnote rows.

Real study reports are full of these and a flat ``df.to_markdown()`` table can show none of them.
One :class:`CTable` spec renders to two twins inside one Quarto cross-reference div:

* an **HTML table** for DOCX. Quarto parses it into a pandoc table, and the DOCX writer emits real
  merged cells (``w:gridSpan`` across, ``w:vMerge`` down);
* a **raw LaTeX table** for PDF (``booktabs`` + ``multirow``, or ruled ``|l|l|`` with
  ``\\cline``). Pandoc's own LaTeX writer collapses spanned tables (tested 2026-10-08), so the
  PDF twin is written here.

Both sit in ``::: {#tbl-x}`` with the caption as its last paragraph, so ``@tbl-x`` resolves in
both formats.

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
import re
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple, Union

CELL_SEP = " | "
_MARK = re.compile(r"\^([^^]+)\^")


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
    style: str = "booktabs"                      # "booktabs" or "grid"
    group_rule: bool = True                      # a rule before each body row that opens a group
    size: str = "small"                          # LaTeX size command for the table body
    resize: bool = True                          # shrink to \linewidth if wider (never enlarges)
    landscape: bool = False                      # PDF: the table on a landscape page of its own
    ncols: int = field(init=False, default=0)

    def __post_init__(self):
        self.header = [[_c(x) for x in r] for r in self.header]
        self.body = [[_c(x) for x in r] for r in self.body]
        self._relabel_notes()
        self.ncols = sum(c.cs for c in self.header[0])
        if not self.label.startswith("tbl-"):
            raise ValueError("label must start with 'tbl-'")
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
    def _latex_rows(self, rows, rule_groups):
        placed, covered = self._grid(rows)
        aligns = self._aligns()
        lines = []
        grid = self.style == "grid"
        # a table is grouped when its first column has a row span somewhere
        grouped = any(c.rs > 1 for cells in placed for col, c in cells if col == 0)
        for r, cells in enumerate(placed):
            starts = dict(cells)
            # the grid style already rules every row, so only booktabs needs a group rule
            if rule_groups and grouped and not grid and r > 0 and (r, 0) not in covered:
                lines.append(r"\hline" if grid else r"\midrule")
            parts, col = [], 0
            while col < self.ncols:
                if col in starts:
                    c = starts[col]
                    txt = _latex(c.text)
                    if r"\newline" in txt and "p{" not in aligns[col]:
                        # a line break in a column that does not wrap (a header, a short label)
                        a_ = (c.align or aligns[col] if len(aligns[col]) == 1 else "l")
                        txt = r"\makecell[" + a_ + "]{" + txt.replace(r"\newline ", r"\\") + "}"
                    if c.rs > 1:
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
                    parts.append("")
                    col += 1
            lines.append(" & ".join(parts) + r" \\")
            if grid:
                # \cline under every column that does not continue a row span into the next row
                spans = [cc for cc in range(self.ncols) if (r + 1, cc) not in covered]
                lines.append(self._clines(spans) if len(spans) < self.ncols else r"\hline")
        return lines, placed

    @staticmethod
    def _clines(cols):
        out, start = [], None
        for i, c in enumerate(cols):
            if start is None:
                start = c
            if i + 1 == len(cols) or cols[i + 1] != c + 1:
                out.append(rf"\cline{{{start + 1}-{c + 1}}}")
                start = None
        return " ".join(out)

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
        grid = self.style == "grid"
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
        hplaced, _ = self._grid(self.header)
        hl, _ = self._latex_rows(self.header, rule_groups=False)
        if not grid:
            out = []
            for r, line in enumerate(hl):
                out.append(line)
                if r + 1 < len(self.header):
                    mids = [rf"\cmidrule(lr){{{col + 1}-{col + c.cs}}}" for col, c in hplaced[r] if c.cs > 1]
                    if mids:
                        out.append(" ".join(mids))
            hl = out
        L += hl
        L.append("" if grid else r"\midrule")
        bl, _ = self._latex_rows(self.body, rule_groups=self.group_rule)
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
