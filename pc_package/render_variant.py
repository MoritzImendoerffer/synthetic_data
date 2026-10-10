#!/usr/bin/env python3
"""Render the corpus a second time with other table rules, without touching the default one.

    python render_variant.py rows                      # every corpus document, as make corpus
    python render_variant.py grid PCP-006_viral_inactivation.qmd INV-002_model_adequacy.DRAFT.qmd
    python render_variant.py rows --jobs 4             # documents in parallel

``rows`` sets a thin rule under every table row and ``grid`` rules every cell; neither rule runs
through a merged cell (``ctable.py`` describes the three styles). The default pass is ``make
corpus`` with ``PC_TABLE_RULES`` unset, and nothing here changes it.

The outputs land in ``variants/<rules>/<name>.docx`` and ``.pdf``, the annexes are copied to
``variants/<rules>/ground_truth/``, and ``check_grounding.py --dir variants/<rules>`` grounds them
(only the annexes of the documents rendered, when a subset is named). Every quote must ground: the
rules change no text, and the DOCX text is what the grounding check reads.

One switch per pass: the environment variable ``PC_TABLE_RULES``. Per document:

* DOCX: ``quarto render --to docx --reference-doc variants/reference_<rules>.docx``. The
  reference document is ``reference.docx`` with borders on its table style "Table", written at
  the start of every pass (``reference_doc``). Quarto wraps every captioned table and figure in a
  one-cell table of the same style, which would draw a frame around caption and table, so that
  container gets explicit empty borders afterwards (``fix_docx``).
* PDF: ``quarto render --to pdf --metadata-file table_rules.yml``. The complex tables read
  ``PC_TABLE_RULES`` in ``ctable.py`` (Quarto's Python kernel inherits the environment), the pipe
  tables get their rules from ``table_rules.lua`` and ``table_rules.tex``, which only this pass
  loads.

Each document is rendered from a staged copy, ``_variant_<rules>_<name>.qmd`` next to the
original, deleted afterwards. Quarto renders next to its input and then moves the result, and both
``--output-dir`` and ``--output`` overwrite and then move away an existing default output of the
same name (tested 2026-10-10); a staged copy under another name leaves the default outputs alone.
The staged name that Quarto writes into figure paths of the DOCX is restored to the real one.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RULES = ("rows", "grid")
#: the documents of a whole pass, in the order make corpus renders them
CORPUS_GLOBS = ("PTP-*.qmd", "RA-*.qmd", "PCMP-*.qmd", "PCP-*.qmd", "PCR-*.qmd", "INV-*.qmd", "PCMR-*.qmd")

# -- the DOCX table style ------------------------------------------------------------------
#: borders of the table style "Table" in each variant, as (OOXML side, size in eighths of a point);
#: a side not named is set to nil. firstRow is the bottom border of the header row, which
#: reference.docx already sets (single, no size) and which is given the inside size here
BORDERS = {
    "rows": {"top": 8, "bottom": 8, "insideH": 4, "firstRow": 4},
    "grid": {"top": 4, "left": 4, "bottom": 4, "right": 4, "insideH": 4, "insideV": 4, "firstRow": 4},
}
_SIDES = ("top", "left", "bottom", "right", "insideH", "insideV")   # the schema order of tblBorders
#: the children of w:tblPr that come after w:tblBorders in the schema order
_AFTER_BORDERS = ("<w:shd", "<w:tblLayout", "<w:tblCellMar", "<w:tblLook", "<w:tblCaption",
                  "<w:tblDescription", "<w:tblPrChange")


def _borders_xml(spec: dict) -> str:
    out = []
    for side in _SIDES:
        sz = spec.get(side)
        out.append(f'<w:{side} w:val="single" w:sz="{sz}" w:space="0" w:color="auto"/>' if sz
                   else f'<w:{side} w:val="nil"/>')
    return "<w:tblBorders>" + "".join(out) + "</w:tblBorders>"


def _put_tbl_borders(tblpr: str, borders: str) -> str:
    """``<w:tblPr>…</w:tblPr>`` with its tblBorders replaced, or inserted in schema order."""
    if "<w:tblBorders" in tblpr:
        return re.sub(r"<w:tblBorders>.*?</w:tblBorders>|<w:tblBorders\s*/>", borders, tblpr, count=1, flags=re.S)
    cut = min([i for i in (tblpr.find(t) for t in _AFTER_BORDERS) if i >= 0] or [tblpr.rindex("</w:tblPr>")])
    return tblpr[:cut] + borders + tblpr[cut:]


def reference_doc(rules: str, out: str) -> str:
    """Write ``reference.docx`` with the borders of ``rules`` on its table style "Table" to ``out``.
    Everything else in the file is copied byte for byte."""
    src = os.path.join(HERE, "reference.docx")
    with zipfile.ZipFile(src) as zin:
        styles = zin.read("word/styles.xml").decode("utf-8")
        m = re.search(r'<w:style [^>]*w:styleId="Table"[^>]*>.*?</w:style>', styles, re.S)
        if not m:
            raise SystemExit("reference.docx has no table style 'Table'")
        style = m.group(0)
        tp = re.search(r"<w:tblPr>.*?</w:tblPr>", style, re.S)
        if not tp:
            raise SystemExit("the table style 'Table' of reference.docx has no w:tblPr")
        new = style[:tp.start()] + _put_tbl_borders(tp.group(0), _borders_xml(BORDERS[rules])) + style[tp.end():]
        sz = BORDERS[rules]["firstRow"]
        new, n = re.subn(r'(<w:tblStylePr w:type="firstRow">.*?<w:tcBorders>\s*)<w:bottom [^>]*/>',
                         rf'\1<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="auto"/>', new, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("the header-row border of the table style 'Table' was not found")
        styles = styles[:m.start()] + new + styles[m.end():]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        _rewrite_zip(zin, out, {"word/styles.xml": styles.encode("utf-8")})
    return out


def _rewrite_zip(zin: zipfile.ZipFile, out: str, replace: dict) -> None:
    tmp = out + ".tmp"
    with zipfile.ZipFile(tmp, "w") as zout:
        for it in zin.infolist():
            zout.writestr(it, replace.get(it.filename, zin.read(it.filename)))
    os.replace(tmp, out)


# -- the float containers of a rendered DOCX -------------------------------------------------
_NIL = _borders_xml({})


def _tables(xml: str):
    """(start, end) of every ``<w:tbl>`` element, nested ones included."""
    out, stack = [], []
    for m in re.finditer(r"<w:tbl>|</w:tbl>", xml):
        if m.group() == "<w:tbl>":
            stack.append(m.start())
        else:
            out.append((stack.pop(), m.end()))
    return out


def _is_container(tbl: str) -> bool:
    """Quarto's frame around a captioned table or figure: one row, one cell, and no header row
    (``w:firstRow="0"``), where every table pandoc writes from a pipe table or an HTML twin has a
    header. Nested tables are blanked out before the rows and cells are counted."""
    own = tbl[len("<w:tbl>"):-len("</w:tbl>")]
    while True:
        inner = _tables(own)
        if not inner:
            break
        s, e = inner[-1]                    # the last to close, with every table it nests
        own = own[:s] + own[e:]
    look = re.search(r"<w:tblLook [^>]*>", own)
    return (len(re.findall(r"<w:tr[ >]", own)) == 1 and len(re.findall(r"<w:tc>", own)) == 1
            and bool(look) and 'w:firstRow="0"' in look.group(0))


def fix_docx(path: str, staged: str, real: str) -> int:
    """Give every float container of a rendered DOCX explicit empty borders, so that the variant
    table style draws no frame around a caption and its table or figure, and put the real name
    back where Quarto wrote the staged one (figure paths in w:docPr/pic:cNvPr ``descr``). Only
    tags and attributes change, never the text the grounding check reads. Returns the number of
    containers."""
    with zipfile.ZipFile(path) as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
        edits = []
        for s, e in _tables(xml):
            if _is_container(xml[s:e]):
                tp = re.compile(r"<w:tblPr>.*?</w:tblPr>", re.S).search(xml, s, e)
                edits.append((tp.start(), tp.end(), _put_tbl_borders(tp.group(0), _NIL)))
        for s, e, rep in sorted(edits, reverse=True):
            xml = xml[:s] + rep + xml[e:]
        xml = xml.replace(staged, real)
        _rewrite_zip(zin, path, {"word/document.xml": xml.encode("utf-8")})
    return len(edits)


# -- rendering -----------------------------------------------------------------------------
def _env(rules: str) -> dict:
    env = dict(os.environ, PC_TABLE_RULES=rules)
    venv = os.path.join(ROOT, ".venv", "bin")
    # Quarto starts its Jupyter kernel with the python3 it finds on PATH (CLAUDE.md, Environment)
    if os.path.isdir(venv) and not env.get("PATH", "").startswith(venv):
        env["PATH"] = venv + os.pathsep + env.get("PATH", "")
    return env


def _quarto(args, env, log):
    r = subprocess.run(["quarto", "render", *args], cwd=HERE, env=env, capture_output=True, text=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"$ quarto render {' '.join(args)}\n{r.stdout}\n{r.stderr}\n")
    return r


def render_one(qmd: str, rules: str, out_dir: str, ref: str) -> tuple:
    """Render one document (docx, then pdf) into ``out_dir``. Returns (name, seconds, error,
    warnings), the warnings being pipe tables that ``table_rules.lua`` left with the default rules."""
    name = os.path.basename(qmd)[:-len(".qmd")]
    staged = f"_variant_{rules}_{name}"
    log = os.path.join(out_dir, f"{name}.log")
    if os.path.exists(log):
        os.remove(log)
    env = _env(rules)
    t0 = time.time()
    shutil.copyfile(qmd, os.path.join(HERE, staged + ".qmd"))
    try:
        r = _quarto([staged + ".qmd", "--to", "docx", "--reference-doc", os.path.relpath(ref, HERE)], env, log)
        if r.returncode:
            return name, time.time() - t0, f"docx render failed (see {os.path.relpath(log, HERE)})", []
        docx = os.path.join(out_dir, name + ".docx")
        shutil.move(os.path.join(HERE, staged + ".docx"), docx)
        fix_docx(docx, staged, name)
        r = _quarto([staged + ".qmd", "--to", "pdf", "--metadata-file", "table_rules.yml"], env, log)
        warns = [ln.strip() for ln in r.stderr.splitlines() if ln.strip().startswith("table_rules.lua:")]
        if r.returncode:
            return name, time.time() - t0, f"pdf render failed (see {os.path.relpath(log, HERE)})", warns
        shutil.move(os.path.join(HERE, staged + ".pdf"), os.path.join(out_dir, name + ".pdf"))
        return name, time.time() - t0, None, warns
    finally:
        for leftover in (".qmd", ".docx", ".pdf", ".tex", ".quarto_ipynb", ".log", ".aux"):
            p = os.path.join(HERE, staged + leftover)
            if os.path.exists(p):
                os.remove(p)
        shutil.rmtree(os.path.join(HERE, staged + "_files"), ignore_errors=True)


def corpus_documents() -> list:
    seen, out = set(), []
    for g in CORPUS_GLOBS:
        for p in sorted(glob.glob(os.path.join(HERE, g))):
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("rules", choices=RULES)
    ap.add_argument("documents", nargs="*", help="qmd files in pc_package/ (default: the whole corpus)")
    ap.add_argument("--jobs", "-j", type=int, default=1, help="documents rendered in parallel")
    ap.add_argument("--no-ground", action="store_true", help="skip copying and grounding the annexes")
    a = ap.parse_args(argv)
    if not shutil.which("quarto"):
        print("FAIL  quarto is not on PATH")
        return 1
    docs = [os.path.join(HERE, os.path.basename(d)) for d in a.documents] or corpus_documents()
    missing = [d for d in docs if not os.path.exists(d)]
    if missing:
        print("FAIL  no such document: " + ", ".join(os.path.basename(d) for d in missing))
        return 1
    out_dir = os.path.join(HERE, "variants", a.rules)
    os.makedirs(out_dir, exist_ok=True)
    ref = reference_doc(a.rules, os.path.join(HERE, "variants", f"reference_{a.rules}.docx"))
    print(f"variant pass PC_TABLE_RULES={a.rules}: {len(docs)} document(s) -> {os.path.relpath(out_dir, ROOT)}/")
    t0, failed = time.time(), []
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        for name, secs, err, warns in ex.map(lambda d: render_one(d, a.rules, out_dir, ref), docs):
            print(f"{'FAIL' if err else 'OK  '}  {name}  {secs:.0f} s" + (f"  {err}" if err else ""))
            for w in warns:
                print(f"      {w}")
            if err:
                failed.append(name)
    print(f"rendered in {time.time() - t0:.0f} s")
    if failed:
        return 1
    if a.no_ground:
        return 0
    # the annexes, grounded against the variant DOCX files: the rules must not change a quote
    gt = os.path.join(out_dir, "ground_truth")
    os.makedirs(gt, exist_ok=True)
    for f in glob.glob(os.path.join(gt, "*.json")):
        os.remove(f)
    import json
    rendered = {os.path.basename(d)[:-len(".qmd")] + ".docx" for d in docs}
    ids = []
    for p in sorted(glob.glob(os.path.join(HERE, "ground_truth", "*.json"))):
        shutil.copy2(p, gt)
        if json.load(open(p, encoding="utf-8")).get("inventory", {}).get("file_name") in rendered:
            ids.append(os.path.basename(p)[:-len(".json")])
    cmd = [sys.executable, os.path.join(HERE, "check_grounding.py"), "--dir", os.path.relpath(out_dir, HERE)]
    if a.documents:
        if not ids:
            print("no annex belongs to the documents rendered; nothing to ground")
            return 0
        for i in ids:
            cmd += ["--doc", i]
    return subprocess.run(cmd, cwd=HERE).returncode


if __name__ == "__main__":
    sys.exit(main())
