# A-Mab Process Characterization — reproducible build
# `make all` regenerates every artifact from the seeded model.

PY := python3
REPORT_DIR := report
QMD := process_characterization.qmd

.PHONY: all data figures report docx pdf fmea test clean env help

help:
	@echo "Targets:"
	@echo "  make all      - data + figures + report (Word & PDF) + FMEA workbook"
	@echo "  make data     - generate datasets       -> outputs/data/"
	@echo "  make figures  - render figures          -> outputs/figures/"
	@echo "  make report   - render Word + PDF        -> report/*.docx, *.pdf"
	@echo "  make fmea     - build post-PC FMEA       -> risk_assessment/*.xlsx"
	@echo "  make test     - run reproducibility tests"
	@echo "  make env      - install Python dependencies"
	@echo "  make clean    - remove generated outputs and rendered documents"

all: report fmea

env:
	$(PY) -m pip install -r requirements.txt

data:
	$(PY) scripts/generate_data.py

figures: data
	$(PY) scripts/make_figures.py

docx: figures
	cd $(REPORT_DIR) && quarto render $(QMD) --to docx

pdf: figures
	cd $(REPORT_DIR) && quarto render $(QMD) --to pdf

report: docx pdf

fmea:
	$(PY) risk_assessment/build_fmea.py

test:
	$(PY) -m pytest -q tests/

clean:
	rm -rf outputs/data/* outputs/figures/* outputs/report_values.json outputs/figure_manifest.json
	rm -f $(REPORT_DIR)/$(QMD:.qmd=.docx) $(REPORT_DIR)/$(QMD:.qmd=.pdf)
	rm -rf $(REPORT_DIR)/.quarto $(REPORT_DIR)/$(QMD:.qmd=_files)
	rm -f risk_assessment/A-Mab_Post-PC_Process_Risk_Assessment.xlsx
	@echo "cleaned."
