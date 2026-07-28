# Runner

> **SUPERSEDED.** Part of the retired two-pass densification workflow — see
> [`README.md`](README.md). Authoring is now one pass, one agent, one context:
> [`../authoring/RUNNER.md`](../authoring/RUNNER.md). Kept as history.

The loop an orchestrating agent executes. Invoke as:

> Execute `ema_docgen/RUNNER.md` for `ema_docgen/docspec/PCR-007.yaml`, tier 1.

---

## Preconditions

- `build/{insertions,review,ledger,state}/` exist
- the target `.qmd` is committed and the working tree is clean
- `make data figures` has been run (the seeded outputs exist)
- `make corpus` has been run at least once, so every document's `.docx` exists
  — `docgen-verify` grounds **all** annexes and fails on any missing render

Abort if the working tree is dirty. Every splice must be revertible.

---

## Loop

```
sections = docspec.sections where tier == <TIER>, in docspec order

for section in sections:
    if state[section.id] == "done": continue

    dispatch AUTHORING_TASK.md in a FRESH subagent, bound with:
        DOC_ID, SOURCE_QMD, SECTION_ID, SECTION_HEADING,
        REGISTER, REQUIRED_MOVES, FORBIDDEN_MOVES

    python ema_docgen/scripts/validate_insertions.py \
        --qmd pc_package/<SOURCE_QMD> \
        --insertions build/insertions/<DOC>/<SECTION>.yaml
    if fail:
        log, mark state "failed", CONTINUE to next section

    python ema_docgen/scripts/splice.py \
        --qmd pc_package/<SOURCE_QMD> \
        --insertions build/insertions/<DOC>/<SECTION>.yaml

    make docgen-verify DOC=<DOC>          # BLOCKING — correctness only
    if fail:
        git checkout -- pc_package/<SOURCE_QMD>
        log, mark state "failed", CONTINUE

    make docgen-report DOC=<DOC>          # ADVISORY — never reverts
        # numerals / wordcount / overlap; note anything worth acting on later,
        # but a LOW word count or a pre-existing bare numeral is NOT a failure
        # of this splice and must not trigger a revert.

    append to build/ledger/<DOC>.md
    mark state "done"

halt and report
```

**Failure policy is continue, not halt.** One bad section should not stop a
tier. Failures accumulate in the state file and are re-run after triage.

**Revert only on `docgen-verify`.** The revert gate is correctness — render,
annex validity, grounding — and nothing else. A spliced-but-*unverifiable*
document must not persist into the next section, or anchors drift and failures
cascade. **Do not revert on `docgen-report`:** its linters measure the whole
document, so mid-densification they legitimately report LOW sections and any
bare numerals that predate the run. Gating reverts on them would revert every
valid splice and the tier would never progress.

---

## Parallelism

Sections within a tier are independent and may be dispatched concurrently.
Sections across tiers may not — tier 1 creates the IDs and facts tiers 2 and 3
cite.

If dispatching in parallel, splice serially afterwards. Concurrent splicing
against the same file will corrupt offsets.

---

## Ledger

After each successful section append to `build/ledger/<DOC>.md`:

```markdown
### <section_id>
- asserts: <one line — the section's principal claim>
- introduces: <IDs first defined here: DEV-007-02, SOP-2011, ...>
- restatable: <claims later sections may restate, one line>
```

Keep to three lines. The ledger is read in full by every subsequent section, so
for a document of ~17 sections it should stay well under 800 words.

**Ledger quality determines whether restatement is real.** Vague entries produce
invented restatements of claims that do not exist, and no gate catches that.
Write `restatable` as a concrete claim, not a topic.

---

## State

`build/state/<DOC>.json`:

```json
{
  "docspec_version": "1",
  "sections": {
    "materials_equipment": {"status": "done", "model": "...", "ts": "..."},
    "results_rsm_aggregate": {"status": "failed", "reason": "3 bare numerals"}
  }
}
```

Record the responding model per section. If part of the corpus came from a
different model than the rest, that is a confound in your own benchmark and
belongs in the release manifest.

Session resume in Claude Code is session-bound and does not survive exit — this
file is the real resumption mechanism.

---

## Halt points

Halt and wait for review:

- at the end of every tier
- after 3 sections on the first run of any new docspec
- if more than a third of a tier's sections fail

Do not proceed past a tier boundary unattended.
