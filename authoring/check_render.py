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
    return segments, chunk_errs, inline_errs


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
