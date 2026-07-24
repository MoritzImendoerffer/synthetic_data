"""Validate every ground-truth annex JSON against the schema.

Re-loads each ``ground_truth/*.json`` from disk and validates it against
``schema_ext.GroundTruthAnnex`` (which composes the nlp_reports app/models
contracts plus this project's local extensions). Exits non-zero on any failure.

Run:  python validate_annex.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

from pydantic import ValidationError

import schema_ext as S

HERE = os.path.dirname(os.path.abspath(__file__))
GT = os.path.join(HERE, "ground_truth")


def main() -> int:
    files = sorted(glob.glob(os.path.join(GT, "*.json")))
    if not files:
        print("no annex files found in", GT)
        return 1
    failures = 0
    for path in files:
        name = os.path.basename(path)
        with open(path) as fh:
            data = json.load(fh)
        try:
            annex = S.GroundTruthAnnex.model_validate(data)
        except ValidationError as exc:
            failures += 1
            print(f"FAIL {name}\n{exc}")
            continue
        n_ent = sum(len(s.process_steps) + len(s.parameters) + len(s.quality_attributes)
                    + len(s.analytical_methods) + len(s.equipment) + len(s.sites)
                    for s in annex.entities)
        n_ass = len(annex.assertions.assertions) if annex.assertions else 0
        n_con = len(annex.concepts.concepts) if annex.concepts else 0
        print(f"OK   {name}: type={annex.inventory.predicted_document_type} "
              f"entities={n_ent} studies={len(annex.studies)} "
              f"design_spaces={len(annex.design_spaces)} assertions={n_ass} concepts={n_con} "
              f"report_stmts={sum(len(rs.statements) for rs in annex.report_sections)}")
    print(f"\n{len(files) - failures}/{len(files)} annexes valid.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
