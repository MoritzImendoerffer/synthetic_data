"""A-Mab drug-substance process model.

A semi-mechanistic, fully reproducible model of the A-Mab (humanized IgG1)
drug-substance process, built to regenerate the data and figures in the process
characterization report and the post-PC FMEA.

Quick start
-----------
>>> from amab_process import Process
>>> proc = Process()
>>> batch = proc.nominal_batch()
>>> round(batch.drug_substance.cqas["aggregates_hmw"], 2)   # doctest: +SKIP
"""

from .config import Config, load_config
from .core import Stream, StepResult, UnitOperation, CQA_UNITS
from .process import Process, BatchResult

__all__ = [
    "Config", "load_config", "Stream", "StepResult", "UnitOperation",
    "CQA_UNITS", "Process", "BatchResult",
]

__version__ = "0.1.0"
