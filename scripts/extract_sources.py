#!/usr/bin/env python3
"""Extract the source PDFs to page-marked plain text (refs/text/).

These extracts are the human-readable basis for the model parameters and the
report/FMEA structure. Re-run after changing the source PDFs.

Usage:  python scripts/extract_sources.py
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {
    "amab": "A-Mab_Case_Study_Version_2-1.pdf",
    "pda_tr60": "pda_60_PV.pdf",
    "ispe_gpg": "2023-ispe-good-practice-guide-practical-implementation-of-the-lifecycle-approach-to-process-validation.pdf",
}


def main() -> None:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF is required: pip install PyMuPDF")

    out_dir = os.path.join(ROOT, "refs", "text")
    os.makedirs(out_dir, exist_ok=True)
    for key, fname in SRC.items():
        path = os.path.join(ROOT, "original_data", fname)
        if not os.path.exists(path):
            print(f"  SKIP {key}: {fname} not found")
            continue
        doc = fitz.open(path)
        out = os.path.join(out_dir, key + ".txt")
        with open(out, "w") as fh:
            for i, page in enumerate(doc, start=1):
                fh.write(f"\n===== [{key}] PAGE {i} =====\n")
                fh.write(page.get_text("text"))
        print(f"  {key:10s} {doc.page_count:4d} pages -> {os.path.relpath(out, ROOT)}")
        doc.close()


if __name__ == "__main__":
    main()
