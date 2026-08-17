# A-Mab Process Characterization — reproducible build
# `make all` regenerates every artifact from the seeded model.

# The interpreter every target runs. Override it for an environment that is not on PATH:
#   make test PY="uv run python"
PY ?= python3
PKG_DIR := pc_package

.PHONY: all data figures fmea corpus style test clean env help pm

help:
	@echo "Targets:"
	@echo "  make all      - data + figures + corpus (documents + ground-truth annexes)"
	@echo "  make data     - generate datasets       -> outputs/data/"
	@echo "  make figures  - render figures          -> outputs/figures/"
	@echo "  make corpus   - render pc_package docs + build/validate ground-truth annexes"
	@echo "  make style    - register gate (plain technical English) over every corpus doc"
	@echo "  make fmea     - build the post-PC FMEA workbook (content source for RA-001)"
	@echo "  make test     - run reproducibility tests"
	@echo "  make pm       - regenerate docs/pm/ (the board) from the active work unit"
	@echo "  make env      - install Python dependencies"
	@echo "  make clean    - remove generated outputs and rendered documents"

all: corpus

env:
	$(PY) -m pip install -r requirements.txt

# Two scripts, in this order, and both are required. generate_superseded.py produces the
# invalidated first execution of the AEX study (DEV-008-01 re-executed it), which PCR-008
# reads, and it patches the dev_scalars / n_deviations entries of report_values.json in
# place. It stays a separate script on purpose -- re-running generate_data.py in a different
# library environment drifts the nominal DoE CSVs in the deep decimals, so this one only
# adds files. It was missing from this target, so `make clean && make data` left
# outputs/data/doe_aex_*_superseded.csv absent and `make corpus` died on PCR-008.
data:
	$(PY) scripts/generate_data.py
	$(PY) scripts/generate_superseded.py

figures: data
	$(PY) scripts/make_figures.py

fmea:
	$(PY) risk_assessment/build_fmea.py

# Register gate over every corpus document: plain technical English, measured against the four
# published human sources (PDA TR 60, A-Mab, and the two 2023 ISPE Good Practice Guides).
# --selftest proves the thresholds are ones real human regulatory prose passes; if it ever
# fails, the threshold is wrong, not the source. A source missing from refs/text/ fails too,
# so a run that measures nothing cannot report the same success as a run that measures four.
style:
	$(PY) authoring/check_style.py --selftest
	$(PY) authoring/check_exemplar_quotes.py
	@rc=0; for f in $(PKG_DIR)/*.qmd; do \
		[ -e "$$f" ] || continue; \
		$(PY) authoring/check_style.py "$$f" || rc=1; \
	done; exit $$rc

# Render every corpus document (docx + pdf) then build & validate the ground-truth
# annexes. All content derives from outputs/, so this stays consistent with the model.
corpus: figures
	@for f in $(PKG_DIR)/PTP-*.qmd $(PKG_DIR)/RA-*.qmd $(PKG_DIR)/PCMP-*.qmd \
	          $(PKG_DIR)/PCP-*.qmd $(PKG_DIR)/PCR-*.qmd $(PKG_DIR)/PCMR-*.qmd; do \
		[ -e "$$f" ] || continue; \
		b=$$(basename $$f); \
		echo "rendering $$b"; \
		( cd $(PKG_DIR) && quarto render "$$b" --to docx && quarto render "$$b" --to pdf ) || exit 1; \
	done
	cd $(PKG_DIR) && $(PY) build_ground_truth.py && $(PY) validate_annex.py && $(PY) check_grounding.py
	@echo "corpus built."

test:
	$(PY) -m pytest -q tests/

# The visible half of the planning workflow: docs/pm/ is .claude/work/<id>/state.json rendered
# as notes a person can read. Generated notes are overwritten; the hand-written ones beside
# them (epic.md, decisions/, the READMEs) are never touched. See docs/PROJECT_WORKFLOW.md.
pm:
	$(PY) scripts/pm_notes.py

clean:
	rm -rf outputs/data/* outputs/figures/* outputs/report_values.json outputs/figure_manifest.json
	rm -f risk_assessment/A-Mab_Post-PC_Process_Risk_Assessment.xlsx
	@# reference.docx is a build INPUT, not an output: every .qmd names it as
	@# `reference-doc:`, and it is not regenerable. A plain `rm -f *.docx` deleted it once
	@# and left `make corpus` failing on all 20 documents with "File 'reference.docx' not
	@# found in resource path". Delete rendered documents by name, never by glob.
	find $(PKG_DIR) -maxdepth 1 -name '*.docx' ! -name 'reference.docx' -delete
	rm -f $(PKG_DIR)/*.pdf
	rm -rf $(PKG_DIR)/.quarto $(PKG_DIR)/*_files $(PKG_DIR)/__pycache__
	@test -f $(PKG_DIR)/reference.docx || { echo "ERROR: clean removed reference.docx"; exit 1; }
	@echo "cleaned."

# ---------------------------------------------------------------------------
# ema_docgen — SUPERSEDED. These targets belong to the retired two-pass
# densification workflow (see ema_docgen/README.md); authoring is now one pass
# via authoring/RUNNER.md. Kept because lint_numerals.py is still used as an
# advisory gate by authoring/check_render.py.
#
#   make docgen-verify DOC=PCR-007   # blocking correctness gate (revert on fail)
#   make docgen-report DOC=PCR-007   # advisory metrics (never fails)
#   make docgen-check  DOC=PCR-007   # both, for a manual end-of-tier look
#
# Deliberately lighter than `make corpus`: renders docx only (which is what
# check_grounding.py reads) and skips pdf, so the per-section gate stays cheap
# enough to run 35 times.
#
# Precondition: run `make corpus` once first, so every document's .docx exists.
# docgen-annex rebuilds and grounds ALL annexes, and check_grounding.py fails on
# any annex whose rendered .docx is missing.
# ---------------------------------------------------------------------------

DOCGEN     := ema_docgen
DOCGEN_PY  := PYTHONPATH=$(DOCGEN)/scripts $(PY)
DOCGEN_QMD  = $(shell $(PY) -c "import yaml;print(yaml.safe_load(open('$(DOCGEN)/docspec/$(DOC).yaml'))['source_qmd'])")

.PHONY: docgen-check docgen-verify docgen-report docgen-render docgen-annex docgen-lint-all

# --- the blocking gate -----------------------------------------------------
# Correctness only: render, rebuild + validate the annexes, and the grounding
# check. These are precisely the properties a valid additive splice must never
# break, so RUNNER.md keys its "revert the splice" decision on THIS target and
# nothing else.
docgen-verify: docgen-render docgen-annex
	@echo "VERIFY-OK  $(DOC)"

# --- the advisory report ---------------------------------------------------
# Never fails the build — every line is '-' prefixed. That is what makes it safe
# to run per-section. The linters measure WHOLE-DOCUMENT state: bare numerals
# that may predate this run, sections still below target while densification is
# in progress (LOW is normal until the last section lands), and source-text
# overlap. None of that is caused by, or a reason to revert, the current splice.
# Read it as a dashboard; do not gate reverts on it.
docgen-report:
	-$(DOCGEN_PY) $(DOCGEN)/scripts/lint_numerals.py $(PKG_DIR)/$(DOCGEN_QMD) \
		--allow-file $(DOCGEN)/numerals.allow
	-$(DOCGEN_PY) $(DOCGEN)/scripts/lint_wordcount.py \
		--docspec $(DOCGEN)/docspec/$(DOC).yaml --qmd $(PKG_DIR)/$(DOCGEN_QMD)
	-$(DOCGEN_PY) $(DOCGEN)/scripts/lint_overlap.py \
		--refs refs/text/*.txt --targets $(PKG_DIR)/$(DOCGEN_QMD) \
		--n 8 --max-hits 10

# --- convenience: both, for a human end-of-tier review ---------------------
# Blocking part first (fails the build on a correctness regression); the
# advisory report runs after and does not change the exit status.
docgen-check: docgen-verify docgen-report
	@echo "PASS   $(DOC) (verify gated; report advisory)"

docgen-render:
	cd $(PKG_DIR) && quarto render "$(DOCGEN_QMD)" --to docx

docgen-annex:
	cd $(PKG_DIR) && $(PY) build_ground_truth.py && $(PY) validate_annex.py
# check_grounding.py is the additive-only enforcement: it fails if any annex
# quote no longer appears verbatim in the rendered .docx.
	cd $(PKG_DIR) && $(PY) check_grounding.py

# Corpus-wide advisory sweep, useful before a release tag.
docgen-lint-all:
	-$(DOCGEN_PY) $(DOCGEN)/scripts/lint_numerals.py $(PKG_DIR)/*.qmd \
		--allow-file $(DOCGEN)/numerals.allow
	-$(DOCGEN_PY) $(DOCGEN)/scripts/lint_overlap.py \
		--refs refs/text/*.txt --targets $(PKG_DIR)/*.qmd --n 8 --max-hits 10
