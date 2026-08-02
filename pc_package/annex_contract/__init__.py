"""The annex contract — the Pydantic models a ground-truth annex is built from.

This package is a **vendored copy**, owned by this repository. It exists so that
``synthetic_data`` builds and validates its annexes with no dependency on any other
project.

Provenance
----------
Copied verbatim from ``nlp_reports/models/`` at commit ``f838645`` (2026-08-02), which
is where these models were first written. Nine modules, the transitive closure of what
``schema_ext.py`` needs::

    base  pharma_entities  inventory  assertions  concepts
    summaries  discourse  results  studies

Nothing was edited on the way in. The files still carry comments that mention
``nlp_reports`` paths; those are upstream's own notes about where a model is consumed,
kept so the copy diffs cleanly against upstream.

Why the copy exists
-------------------
The dependency used to run the wrong way. ``schema_ext.py`` put a sibling checkout on
``sys.path`` (``NLP_REPORTS_PATH``, defaulting to a hard-coded home directory) and
imported ``app.models.*`` from it. That made this repo unbuildable on any machine
without that checkout, and it broke outright when upstream renamed its import package
from ``app`` to ``nlp_reports``: ``validate_annex.py`` died with ``ModuleNotFoundError``
while every other gate stayed green, so the corpus looked healthy and was not being
schema-checked at all.

The direction is now the only one that makes sense. ``nlp_reports`` consumes this
corpus — it carries this repository as ``external/synthetic_data`` — so this repository
must not reach back into it. The published artifact is the annex **JSON**, and the JSON
is the real contract; these classes are just how this repo emits and checks it.

Keeping it in step with upstream
--------------------------------
Not automatic, and deliberately so: a consumer's refactor must not be able to break this
build again. To resync, re-copy the nine modules and re-run
``build_ground_truth.py && validate_annex.py``. The annex JSON must come out unchanged;
if it does not, the contract changed and that is a decision to make, not a copy to
apply. Local widenings and additions never go here — they belong in ``schema_ext.py``,
which is the one place this repo departs from the contract and says why.
"""
