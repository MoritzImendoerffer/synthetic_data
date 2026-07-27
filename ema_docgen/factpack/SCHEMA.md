# Fact pack schema

`ema_docgen/factpack/<DOC_ID>/<SECTION_ID>.yaml`

The set of facts a section may use. The agent may use nothing else.

An **empty stub already exists for every section of every document** — 459 of
them, created by `scripts/init_factpacks.py`. An empty fact pack is valid and
means the section may state nothing beyond what the document and the helpers
already provide, which is the correct setting for most analytical sections.
Fill in the ones that need facts; leave the rest alone.

`PCR-007/dev_01.yaml` and `PCR-007/dev_02.yaml` are worked examples; every other
fact pack ships as an empty stub.
`_TEMPLATE.yaml` is the blank form.

**This is the binding constraint on output quality.** You cannot write more
words about the same facts without padding. If the pilot returns a wall of
`<<NEEDS:>>`, the work is in `amab_process/`, not in the prompt.

---

## Structure

```yaml
doc_id: PCR-007
section_id: deviations
facts:
  - id: DEV-007-02
    type: deviation
    ...
```

`id` is what later sections cite. Every fact that introduces an identifier
creates a multi-hop retrieval hook — this is where benchmark difficulty comes
from, not from prose length.

---

## Types

| Type | Fields |
|---|---|
| `deviation` | `description`, `detected_during`, `investigation`, `root_cause`, `impact_on_conclusion`, `disposition` |
| `excluded_run` | `run_number`, `response`, `basis` (statistical test + result), `effect_of_exclusion` |
| `equipment` | `identifier`, `description`, `calibration_status`, `calibration_due` |
| `lot` | `identifier`, `material`, `vendor`, `expiry`, `used_in` |
| `method_performance` | `method_id`, `accuracy`, `precision`, `loq`, `lod`, `variance_contribution` |
| `equivalence_test` | `attribute`, `test`, `result`, `passed` (bool), `justification_if_failed` |
| `prior_doc` | `identifier`, `title`, `date`, `decision_taken` |
| `incident` | `description`, `date`, `resolution` |

All values are strings unless noted. Numerics go in as helper expression names,
not literals — see below.

---

## Numerics

Facts carry **names of helper expressions**, not numbers:

```yaml
  - id: DEV-007-02
    type: deviation
    description: >-
      Column inlet temperature excursion during run 14 of the response-surface
      design.
    detected_during: rsm_execution
    investigation: >-
      Chamber controller fault; excursion bounded and duration recorded.
    root_cause: controller_setpoint_drift
    impact_on_conclusion: >-
      Run retained. Temperature was not a factor in this design and the
      excursion is within the univariate range assessed in PCP-007.
    disposition: retained
    values:
      excursion_max: dev_007_02_tmax     # -> `{python} dev_007_02_tmax`
      excursion_min: dev_007_02_duration
```

If a helper does not yet exist for a value, leave the name in anyway and let
the agent emit `<<NEEDS:>>`. That is the signal to extend the generator.

---

## Availability

```yaml
  - id: LOT-RES-4471
    type: lot
    material: cation-exchange resin
    ...
    available_for: [materials_equipment, resin_reuse, deviations]
```

Optional. Omit to make a fact available to every section in the document.

Use it to force multi-hop: a lot introduced in `materials_equipment` and cited
in `resin_reuse` requires the retriever to connect two distant sections.

---

## Mining A-Mab for facts

A-Mab is a legitimate and valuable source for fact *content* — linkage tables
with per-step attribute states, batch histories, platform ranges, prior-knowledge
claims, viral clearance factors. That is what it was published for.

Take the facts. Do not take the sentences. See DESIGN.md R1.
