#!/usr/bin/env python3
"""Dry-render gate for a one-pass authored ``.qmd`` — the correctness check.

    uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.qmd
    uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.qmd --render

It replicates **Quarto's Python execution model**: all ``{python}`` code runs top-to-bottom
in ONE shared namespace, so an inline expression near the end of a document depends on names
bound in the setup chunk (and anywhere above it). The gate therefore:

  1. parses the document in order, interleaving fenced ``{python}`` chunks and inline
     `` `{python} EXPR` `` expressions;
  2. execs each chunk and evals each inline expression against a single accumulating
     namespace, with cwd = the document's directory (so ``from _pcpkg import *``,
     ``../outputs/...`` and ``reference.docx`` resolve exactly as under Quarto);
  3. reports any NameError / bad-helper-call / typo, and any ``<<NEEDS:>>`` gap markers;
  4. runs the bare-numeral lint (``ema_docgen/scripts/lint_numerals.py``, advisory);
  5. runs the register gate (``authoring/check_style.py``, hard) — sentence-length
     distribution, punctuation habits and banned tics, with thresholds calibrated so that
     PDA TR 60 and the A-Mab case study pass them.

With ``--render`` it additionally runs the real ``quarto render --to docx`` when quarto is
present (the truest gate). Grounding (annex ↔ document) is a SEPARATE, later step
(``check_grounding.py`` after the annex is built) — it is deliberately not run here, because
at authoring time no annex exists yet.

Exit 0 iff every chunk execs, every inline expression evals, there are no ``<<NEEDS:>>``
markers, the numeral lint passes, and (with ``--render``) quarto succeeds.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LINT = os.path.join(ROOT, "ema_docgen", "scripts", "lint_numerals.py")
STYLE = os.path.join(HERE, "check_style.py")

INLINE_RE = re.compile(r"`\{python\}\s*(.+?)`")
NEEDS_RE = re.compile(r"<<NEEDS:[^>]*>>")
FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def blank_comments(text: str) -> str:
    """Replace each HTML/Quarto `<!-- ... -->` comment with an equal number of newlines.
    Quarto does not render comments, so the gate must not exec, eval, or lint their
    contents — while preserving line numbers for accurate error reporting."""
    return COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def parse_segments(text: str):
    """Ordered list of ('chunk', code, lineno) and ('inline', expr, lineno), matching
    Quarto's top-to-bottom execution. Inline expressions inside fenced blocks are ignored
    (a ```{python} fence must not be mistaken for an inline `{python}` span)."""
    segments = []
    in_fence = False
    fence_lang = ""
    buf: list[str] = []
    start = 0
    for i, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            if not in_fence:
                in_fence, fence_lang, buf, start = True, line.strip()[3:].strip(), [], i + 1
            else:
                if fence_lang.startswith("{python"):
                    segments.append(("chunk", "\n".join(buf), start))
                in_fence, fence_lang, buf = False, "", []
            continue
        if in_fence:
            buf.append(line)
        else:
            for m in INLINE_RE.finditer(line):
                segments.append(("inline", m.group(1), i))
    return segments


def dry_run(qmd: str):
    """Exec chunks / eval inline exprs in one namespace. Returns (chunk_errs, inline_errs)."""
    text = blank_comments(open(qmd, encoding="utf-8").read())
    segments = parse_segments(text)
    ns: dict = {"__name__": "__main__"}
    chunk_errs, inline_errs = [], []
    prev_cwd = os.getcwd()
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.chdir(os.path.dirname(os.path.abspath(qmd)))
    sink = io.StringIO()  # discard the document's own printed output (asis chunks)
    try:
        with contextlib.redirect_stdout(sink):
            for kind, code, ln in segments:
                if kind == "chunk":
                    try:
                        exec(compile(code, f"<chunk@L{ln}>", "exec"), ns)
                    except Exception as e:  # noqa: BLE001
                        chunk_errs.append((ln, code, e, traceback.format_exc()))
                        break  # a failed chunk corrupts every downstream name; stop
                else:
                    try:
                        eval(compile(code, f"<inline@L{ln}>", "eval"), ns)
                    except Exception as e:  # noqa: BLE001
                        inline_errs.append((ln, code, e))
    finally:
        os.chdir(prev_cwd)
    _LAST_NS[os.path.abspath(qmd)] = ns
    return segments, chunk_errs, inline_errs


# the namespace of the last dry run per document, so the table-fit check can evaluate a builder
# call that uses the document's own variables (T.frame(design_tab, ...))
_LAST_NS: dict = {}


def run_lint(qmd: str) -> int:
    if not os.path.exists(LINT):
        print("WARN  numeral lint not found; skipping")
        return 0
    # Run from repo root so the default allow-file (ema_docgen/numerals.allow) resolves;
    # the script's own dir is on sys.path[0], so its `_common` import works.
    rel = os.path.relpath(os.path.abspath(qmd), ROOT)
    r = subprocess.run([sys.executable, LINT, rel], cwd=ROOT,
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.stderr.strip():
        sys.stderr.write(r.stderr)
    return r.returncode


def run_style(qmd: str) -> int:
    """Register gate — plain technical English, measured against the human sources."""
    if not os.path.exists(STYLE):
        print("WARN  style gate not found; skipping")
        return 0
    r = subprocess.run([sys.executable, STYLE, os.path.abspath(qmd)],
                       cwd=ROOT, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.stderr.strip():
        sys.stderr.write(r.stderr)
    return r.returncode


def check_pdf_glyphs(qmd: str) -> int:
    """Fail if the rendered PDF contains missing-glyph boxes.

    The LaTeX text font has no glyph for several characters the corpus uses — the maths
    operators and the Unicode sub/superscripts in things like ``log₁₀`` and ``pCO₂``. They
    render as NULL, so ``≥ 4.93`` becomes ``␀ 4.93``: a clearance *floor* silently reads as
    a point value, which inverts an acceptance criterion. The docx pipeline is unaffected,
    which is why this shipped unnoticed across eight documents — nothing ever looked at the
    PDF after rendering. The fix is the Unicode font block in the document's pdf format
    (mainfont/sansfont/monofont/mathfont); this check makes its absence loud.
    """
    pdf = os.path.splitext(os.path.abspath(qmd))[0] + ".pdf"
    if not os.path.exists(pdf):
        return 0
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("WARN  PyMuPDF not available; skipping PDF glyph check")
        return 0
    doc = fitz.open(pdf)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    n = text.count("\x00")
    if n:
        print(f"FAIL  {os.path.basename(pdf)}: {n} missing glyph(s) in the rendered PDF.")
        print("      Add the Unicode font block to the pdf: format "
              "(mainfont/sansfont/monofont/mathfont: DejaVu …) and re-render.")
        return 1
    print(f"OK    {os.path.basename(pdf)}: no missing glyphs")
    return 0


def check_tables_fit(qmd: str) -> int:
    """Fail if a complex table is cut off in the rendered PDF.

    A raw-LaTeX table sits in a float, and a float cannot break across pages. A table taller
    than a page therefore runs off the bottom silently: its last rows and its footnotes are
    simply not in the PDF. Found 2026-10-08 on INV-001, whose Version 1.0 / Version 2.0 table
    lost its last two rows and both footnotes. This evaluates every ``T.<builder>(...)`` call
    the document prints and requires the text of its last body row and of its last footnote
    to appear in the PDF. The DOCX is unaffected, so only the PDF is checked.
    """
    pdf = os.path.splitext(os.path.abspath(qmd))[0] + ".pdf"
    if not os.path.exists(pdf) or os.path.getmtime(pdf) < os.path.getmtime(qmd):
        return 0
    calls = re.findall(r"(T\.\w+\((?:[^()]|\([^()]*\))*\))\.show\(\)", open(qmd, encoding="utf-8").read())
    if not calls:
        return 0
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return 0
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    import tables as T  # noqa: E402
    doc = fitz.open(pdf)
    text = re.sub(r"\s+", " ", " ".join(page.get_text() for page in doc))
    doc.close()
    bad = []
    # the document's namespace from the dry run where there was one, else its identity variables
    ns = dict(_LAST_NS.get(os.path.abspath(qmd), {}))
    ns["T"] = T
    for m in re.finditer(r'^(DOC|UO|UO_TITLE)\s*=\s*(.+)$', open(qmd, encoding="utf-8").read(), re.M):
        try:
            ns[m.group(1)] = eval(m.group(2), {})
        except Exception:  # noqa: BLE001
            pass
    for c in calls:
        try:
            t = eval(c, ns)
        except Exception as e:  # noqa: BLE001
            bad.append(f"{c}: cannot evaluate ({e})")
            continue
        # the last cell's own text, without footnote markers: a superscript marker runs into
        # its word in the PDF text layer ("no DoEe)"), so it cannot be part of the probe
        last = t.body[-1][-1]
        frags = [f.strip(" ,;") for f in re.split(r"\^[^^]+\^", str(getattr(last, "text", last)))]
        probes = [max(frags, key=len)]
        if t.notes:
            probes.append(t.notes[-1][1][:40])
        for pr in probes:
            pr = re.sub(r"\s+", " ", pr).strip()
            if pr and pr not in text:
                bad.append(f"{t.label}: {pr[:50]!r} not in the PDF (table taller than a page?)")
    if bad:
        print(f"FAIL  {len(bad)} complex table(s) cut off in the PDF:")
        for b in bad:
            print(f"      {b}")
        return 1
    print(f"OK    {len(calls)} complex table(s) complete in the PDF")
    return 0


# The smallest text a table may print, in points. Owner's comment 2026-10-08: "an acceptable level of
# font reduction is used in Table 5.6 [of PCR-005] but it should not be more than that". That table
# prints at 8.1 pt against 10.9 pt body text, which is \scriptsize with no further shrink.
FONT_FLOOR_PT = 7.9


def check_font_floor(qmd: str) -> int:
    """Fail if any text in the PDF is set below FONT_FLOOR_PT: a table shrunk to fit its page.

    A table wider than the text block is shrunk by adjustbox, and its text with it. Below the floor
    the table needs abbreviated headers (defined in its note and in the Abbreviations table), line
    breaks in its headers, fewer or narrower columns, or a landscape page of its own
    (``CTable(landscape=True)``). Superscripts (footnote markers) are exempt."""
    pdf = os.path.splitext(os.path.abspath(qmd))[0] + ".pdf"
    if not os.path.exists(pdf) or os.path.getmtime(pdf) < os.path.getmtime(qmd):
        return 0
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return 0
    doc = fitz.open(pdf)
    bad = {}
    for pno, page in enumerate(doc):
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    # a superscript (footnote marker) is meant to be small: flag bit 0
                    tx = sp["text"].strip()
                    if (len(tx) > 2 and not sp["flags"] & 1 and not re.fullmatch(r"[A-Za-z]{1,2}\d?\)", tx)
                            and sp["size"] < FONT_FLOOR_PT):
                        bad.setdefault(pno + 1, (sp["size"], sp["text"].strip()[:40]))
    doc.close()
    if bad:
        print(f"FAIL  text below {FONT_FLOOR_PT} pt on {len(bad)} page(s) (a table shrunk too far: "
              "abbreviate or break its headers, or set it landscape):")
        for pg, (sz, tx) in sorted(bad.items()):
            print(f"      p.{pg}: {sz:.1f} pt, {tx!r}")
        return 1
    print(f"OK    no text below {FONT_FLOOR_PT} pt")
    return 0


# tables whose first column legitimately repeats: the approval record (one signature per row)
_MERGE_EXEMPT_HEADERS = ("Role",)


def docx_tables(docx: str):
    """[(caption-less header cells, [[cell text, ...], ...]), ...] for every table in a DOCX. A
    vertically merged continuation cell reads as the empty string."""
    import html as _html
    import zipfile
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    out = []
    for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", xml, re.S):
        rows = []
        for tr in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S):
            cells = [re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", tc))).strip()
                     for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, re.S)]
            rows.append(cells)
        # a pipe table's caption is written into the table as its first row
        if rows and len(rows[0]) == 1 and re.match(r"Table \d+", rows[0][0]):
            rows = rows[1:]
        if rows:
            out.append((rows[0], rows[1:]))
    return out


def check_table_merges(qmd: str) -> int:
    """Fail if a table repeats its index cell down consecutive rows instead of merging it.

    Owner's comment 2026-10-08: index cells that repeat across rows are merged, as a report sets
    them. A pipe table (``df.to_markdown()``, ``md()``) cannot merge, so a table whose first column
    repeats is built with ``T.frame(df, merge=[...])`` or a builder in tables.py. Reads the DOCX,
    where a merged continuation cell is empty."""
    docx = os.path.splitext(os.path.abspath(qmd))[0] + ".docx"
    if not os.path.exists(docx) or os.path.getmtime(docx) < os.path.getmtime(qmd):
        return 0
    bad = []
    for head, rows in docx_tables(docx):
        # a captioned pipe table carries its caption in front of the first header cell
        first = re.sub(r"^Table \d+:.*?\.\s+", "", head[0]) if head else ""
        if not head or first in _MERGE_EXEMPT_HEADERS or len(rows) < 2:
            continue
        reps = [r[0] for a, r in zip(rows, rows[1:]) if r and a and r[0] and r[0] == a[0]
                and len(r) > 1]
        if reps:
            bad.append(f"table headed {' | '.join(head)[:60]!r}: first cell {reps[0]!r} repeats")
    if bad:
        print(f"FAIL  {len(bad)} table(s) repeat an index cell instead of merging it "
              "(use T.frame(df, merge=[...])):")
        for b in bad:
            print(f"      {b}")
        return 1
    print("OK    no table repeats an index cell down its rows")
    return 0


def run_quarto(qmd: str) -> int:
    if not shutil.which("quarto"):
        print("WARN  --render requested but quarto not on PATH; skipping real render")
        return 0
    print(f"\n=== quarto render {os.path.basename(qmd)} --to docx ===")
    r = subprocess.run(["quarto", "render", os.path.basename(qmd), "--to", "docx"],
                       cwd=os.path.dirname(os.path.abspath(qmd)),
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stdout.write(r.stdout[-4000:])
        sys.stderr.write(r.stderr[-4000:])
        print("FAIL  quarto render errored")
    else:
        print("OK    quarto render succeeded")
    return r.returncode


def check(qmd: str, do_render: bool, strict_numerals: bool, lax_style: bool) -> int:
    text = blank_comments(open(qmd, encoding="utf-8").read())
    segments, chunk_errs, inline_errs = dry_run(qmd)
    n_chunk = sum(1 for s in segments if s[0] == "chunk")
    n_inline = sum(1 for s in segments if s[0] == "inline")
    needs = NEEDS_RE.findall(text)

    print(f"== {os.path.relpath(qmd, ROOT)} ==")
    print(f"   {n_chunk} python chunk(s), {n_inline} inline expression(s)")

    ok = True
    for ln, code, e, tb in chunk_errs:
        ok = False
        head = code.strip().splitlines()[0][:70] if code.strip() else ""
        print(f"FAIL  chunk @L{ln} ({head!r}...): {type(e).__name__}: {e}")
        print("      " + tb.strip().splitlines()[-1])
    for ln, code, e in inline_errs:
        ok = False
        print(f"FAIL  inline @L{ln}: `{{python}} {code}`  -> {type(e).__name__}: {e}")
    if needs:
        ok = False
        print(f"NEEDS {len(needs)} unresolved marker(s):")
        for n in needs[:20]:
            print(f"      {n}")
    if not chunk_errs and not inline_errs and not needs:
        print("OK    all chunks exec, all inline expressions eval, no <<NEEDS:>> markers")

    # Numeral lint is ADVISORY by default (the committed corpus itself carries a few
    # statistical conventions — alpha=0.05, p<0.05, n=4, 95% CI — that the allow-file
    # deliberately does not exempt). It flags candidates for the author to convert to
    # inline expressions; it does not fail the correctness gate unless --strict-numerals.
    print(f"\n=== numeral lint ({'GATE' if strict_numerals else 'advisory'}) ===")
    lint_rc = run_lint(qmd)

    # The register gate IS hard by default: a document in the wrong voice is a defect,
    # and the thresholds are calibrated so real human regulatory prose passes them
    # (check_style.py --selftest). --lax-style demotes it while drafting.
    print(f"\n=== register / style ({'advisory' if lax_style else 'GATE'}) ===")
    style_rc = run_style(qmd)

    render_rc = run_quarto(qmd) if do_render else 0
    if render_rc == 0:
        render_rc = check_pdf_glyphs(qmd)
    if render_rc == 0:
        render_rc = check_tables_fit(qmd)
    if render_rc == 0:
        render_rc = check_table_merges(qmd)
    if render_rc == 0:
        render_rc = check_font_floor(qmd)

    hard_ok = (ok and render_rc == 0
               and (lint_rc == 0 or not strict_numerals)
               and (style_rc == 0 or lax_style))
    if lint_rc != 0 and not strict_numerals:
        print("      ^ advisory: convert any TYPED MEASUREMENT above into an inline "
              "expression; statistical conventions (α, p-thresholds, n, CI level) may stay.")
    return 0 if hard_ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("qmd", nargs="+")
    ap.add_argument("--render", action="store_true",
                    help="also run the real `quarto render --to docx` when quarto is present")
    ap.add_argument("--strict-numerals", action="store_true",
                    help="promote the numeral lint to a hard gate (default: advisory)")
    ap.add_argument("--lax-style", action="store_true",
                    help="demote the register gate to advisory (default: hard gate)")
    args = ap.parse_args()
    rc = 0
    for q in args.qmd:
        if not os.path.exists(q):
            print(f"FAIL  no such file: {q}")
            rc = 1
            continue
        rc = max(rc, check(q, args.render, args.strict_numerals, args.lax_style))
    return rc


if __name__ == "__main__":
    sys.exit(main())
