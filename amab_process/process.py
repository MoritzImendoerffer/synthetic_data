"""Full A-Mab drug-substance process train.

Chains the eight modelled unit operations and returns per-step results plus the
final drug-substance stream. A single master-seeded RNG makes every batch, DoE
run and Monte-Carlo campaign fully reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from .config import Config, load_config
from .core import Stream, StepResult
from .unit_ops import (AEX, CEX, Bioreactor, Harvest, ProteinA, UFDF,
                       ViralInactivation, VirusFiltration)

# processing order with stable string keys
_TRAIN = [
    ("bioreactor", Bioreactor),
    ("harvest", Harvest),
    ("protein_a", ProteinA),
    ("viral_inactivation", ViralInactivation),
    ("cex", CEX),
    ("aex", AEX),
    ("virus_filtration", VirusFiltration),
    ("ufdf", UFDF),
]


@dataclass
class BatchResult:
    """Outcome of one full drug-substance batch."""

    steps: List[StepResult]
    drug_substance: Stream
    overall_yield: float
    setpoints: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def step(self, key_or_name: str) -> StepResult:
        for i, (k, _) in enumerate(_TRAIN):
            if k == key_or_name:
                return self.steps[i]
        for s in self.steps:
            if s.step == key_or_name:
                return s
        raise KeyError(key_or_name)

    @property
    def cqas(self) -> Dict[str, float]:
        return dict(self.drug_substance.cqas)


class Process:
    """The A-Mab drug-substance process."""

    def __init__(self, cfg: Optional[Config] = None):
        self.cfg = cfg or load_config()
        self.units = [(k, cls(self.cfg)) for k, cls in _TRAIN]

    def rng(self, offset: int = 0) -> np.random.Generator:
        return np.random.default_rng(self.cfg.seed + offset)

    def run_batch(self, rng: np.random.Generator,
                  overrides: Optional[Dict[str, Dict[str, float]]] = None) -> BatchResult:
        """Run one batch. ``overrides`` maps unit-op key -> {param: natural value}."""
        overrides = overrides or {}
        stream: Optional[Stream] = None
        steps: List[StepResult] = []
        used_setpoints: Dict[str, Dict[str, float]] = {}
        first_mass = None
        for key, unit in self.units:
            res = unit.run(stream, rng, setpoints=overrides.get(key))
            steps.append(res)
            used_setpoints[key] = res.params
            stream = res.out
            if first_mass is None:
                first_mass = res.out.product_mass_g
        overall_yield = stream.product_mass_g / first_mass if first_mass else float("nan")
        return BatchResult(steps=steps, drug_substance=stream,
                           overall_yield=overall_yield, setpoints=used_setpoints)

    def nominal_batch(self, offset: int = 0) -> BatchResult:
        """Run the process at set-points (no parameter overrides)."""
        return self.run_batch(self.rng(offset))
