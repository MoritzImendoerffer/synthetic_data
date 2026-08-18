# TASK-001 procedure — one gated mechanism for the rhetorical layer

**Pure refactor. It must not change one byte of any annex.** That is both the acceptance criterion
and the only reason to do it before any document is re-authored: afterwards there is no
byte-identical baseline left to prove it against.

## What exists today

| document | spans | source |
|---|---|---|
| PCR-003 | 35 | `authoring/rhetorical/PCR-003.spans.yaml`, hard-gated by `build_rhetorical_annex.py` |
| PCR-004 | 36 | `h_rhetorical_spans()` + `H_RHET_SPANS` in `build_ground_truth.py` |
| PCR-005 | 39 | `pa_rhetorical_spans()` |
| PCR-006 | 31 | `vi_rhetorical_spans()` |
| PCR-007 | 33 | `cx_rhetorical_spans()` |
| PCR-008 | 25 | `ax_rhetorical_spans()` |
| PCR-009 | 37 | `vf_rhetorical_spans()` |
| PCR-010 | 30 | `uf_rhetorical_spans()` |
| PCMR-001 | 49 | `pcmr_rhetorical_spans()` |

The eight Python builders emit **every** span unconditionally — there is no presence check, so a
stale quote is caught only later by `check_grounding.py`. The YAML path skips a missing span with a
warning inside `build_ground_truth.py`, and `build_rhetorical_annex.py` fails hard on it. After
this task there is one path and one behaviour.

## Steps

1. **Snapshot the baseline** — `cp -r pc_package/ground_truth /tmp/gt-before` — so step 4 can prove
   byte-identity even if something is committed in between.
2. **Emit the YAML from the code, do not retype it.** Write a throwaway script that imports
   `build_ground_truth`, calls each `*_rhetorical_spans(doc_id, file_name)`, and dumps
   `id / section / role / quote / supported_by / restates / bounds` into
   `authoring/rhetorical/<DOC>.spans.yaml` in the shape `PCR-003.spans.yaml` already uses. Retyping
   315 spans by hand is how a quote acquires a typo that grounds nowhere.
   **The span ids in the YAML are the suffixes**: the builders emit `f"{doc_id}-{suffix}"`, and
   `build_rhetorical_spans` does the same, so the YAML carries the suffix and not the full id.
3. **Delete the eight builders and their `*_RHET_SPANS` tables**, and route those documents through
   `build_rhetorical_spans()` — the same call `PCR-003` already uses.
4. **Prove it changed nothing.**
   ```bash
   cd pc_package && uv run python build_ground_truth.py && cd ..
   git diff --stat pc_package/ground_truth/       # MUST be empty
   diff -r /tmp/gt-before pc_package/ground_truth # MUST be silent
   ```
   A non-empty diff means the conversion lost or reordered something. Find it; do not accept it.
5. **Prove the gate now covers all nine.**
   ```bash
   for d in PCR-003 PCR-004 PCR-005 PCR-006 PCR-007 PCR-008 PCR-009 PCR-010 PCMR-001; do
     f=$(ls pc_package/${d}_*.docx | head -1)
     uv run python authoring/build_rhetorical_annex.py --doc $d --file "$f" | tail -2
   done
   ```
   Expect 35 / 36 / 39 / 31 / 33 / 25 / 37 / 30 / 49, none dropped.
6. `uv run python validate_annex.py` → 20/20; `GROUNDING_STRICT_ANCHORS=1 uv run python
   check_grounding.py` → 2084/2084, 0 weak anchors; `make test` 89; `make style` 24 OK / 0 FAIL.

## Do not

Extend the layer to the eleven documents that have none. That is
`docs/next/rhetorical-layer-coverage.md` and it is a different argument. This task unifies the
mechanism for the nine that have one, which is half of that proposal and is recorded as such at
ship.
