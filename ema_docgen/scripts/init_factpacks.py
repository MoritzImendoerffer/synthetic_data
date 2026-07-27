#!/usr/bin/env python3
"""Create an empty fact-pack stub for every section in a docspec.

Run once after installing, so the runner never fails on a missing fact pack.
Existing files are never overwritten.

    python init_factpacks.py ema_docgen/docspec/*.yaml
    python init_factpacks.py ema_docgen/docspec/PCR-007.yaml --root ema_docgen
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

STUB = """# Facts available to {doc_id} / {section_id}.
#
# Empty is valid: it means this section may state nothing that is not already in
# the document or available from a helper. Correct for most analytical sections.
#
# See ../_TEMPLATE.yaml for the field reference.
#
#   heading:  {heading}
#   register: {register}
#   tier:     {tier}

doc_id: {doc_id}
section_id: {section_id}

facts: []
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("docspecs", nargs="+", type=Path)
    ap.add_argument("--root", type=Path, default=None,
                    help="module root; defaults to the docspec's parent's parent")
    args = ap.parse_args()

    made = skipped = 0
    for spec_path in args.docspecs:
        if spec_path.name.startswith("_"):
            continue
        spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        root = args.root or spec_path.parent.parent
        doc_id = spec["doc_id"]
        out_dir = root / "factpack" / doc_id
        out_dir.mkdir(parents=True, exist_ok=True)

        for sec in spec.get("sections", []):
            target = out_dir / f"{sec['id']}.yaml"
            if target.exists():
                skipped += 1
                continue
            target.write_text(STUB.format(
                doc_id=doc_id,
                section_id=sec["id"],
                heading=sec.get("heading", ""),
                register=sec.get("register", ""),
                tier=sec.get("tier", ""),
            ), encoding="utf-8")
            made += 1

    print(f"OK     {made} stub(s) created, {skipped} left alone")
    return 0


if __name__ == "__main__":
    sys.exit(main())
