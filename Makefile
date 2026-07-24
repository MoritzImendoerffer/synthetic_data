# A-Mab Process Characterization — reproducible build
# `make all` regenerates every artifact from the seeded model.

PY := python3
PKG_DIR := pc_package

.PHONY: all data figures fmea corpus test clean env help

help:
	@echo "Targets:"
	@echo "  make all      - data + figures + corpus (documents + ground-truth annexes)"
	@echo "  make data     - generate datasets       -> outputs/data/"
	@echo "  make figures  - render figures          -> outputs/figures/"
	@echo "  make corpus   - render pc_package docs + build/validate ground-truth annexes"
	@echo "  make fmea     - build the post-PC FMEA workbook (content source for RA-001)"
	@echo "  make test     - run reproducibility tests"
	@echo "  make env      - install Python dependencies"
	@echo "  make clean    - remove generated outputs and rendered documents"

all: corpus

env:
	$(PY) -m pip install -r requirements.txt

data:
	$(PY) scripts/generate_data.py

figures: data
	$(PY) scripts/make_figures.py

fmea:
	$(PY) risk_assessment/build_fmea.py

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
	cd $(PKG_DIR) && $(PY) build_ground_truth.py && $(PY) validate_annex.py
	@echo "corpus built."

test:
	$(PY) -m pytest -q tests/

clean:
	rm -rf outputs/data/* outputs/figures/* outputs/report_values.json outputs/figure_manifest.json
	rm -f risk_assessment/A-Mab_Post-PC_Process_Risk_Assessment.xlsx
	rm -f $(PKG_DIR)/*.docx $(PKG_DIR)/*.pdf
	rm -rf $(PKG_DIR)/.quarto $(PKG_DIR)/*_files $(PKG_DIR)/__pycache__
	@echo "cleaned."
