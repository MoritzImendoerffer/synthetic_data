"""Configuration loader for the A-Mab process model.

Loads ``config/parameters.yaml`` into lightweight accessor objects. The YAML is
the single numeric source of truth shared by the model, the report and the FMEA.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_CFG = os.path.normpath(os.path.join(_HERE, "..", "config", "parameters.yaml"))


@dataclass
class Parameter:
    key: str
    name: str
    unit: str
    setpoint: float
    classification: str
    study: str
    prange: List[float]              # characterization / DoE edges [lo, hi]
    nor: List[float]                 # normal operating range [lo, hi]

    @property
    def par(self) -> List[float]:
        """Proven acceptable range (the characterized range)."""
        return self.prange


@dataclass
class UnitOpConfig:
    key: str
    step: int
    name: str
    parameters: List[Parameter]
    raw: Dict[str, Any]

    def param(self, key: str) -> Parameter:
        for p in self.parameters:
            if p.key == key:
                return p
        raise KeyError(f"{self.key}: no parameter {key!r}")

    @property
    def model(self) -> Dict[str, Any]:
        return self.raw.get("model", {})


class Config:
    """Top-level configuration accessor."""

    def __init__(self, data: Dict[str, Any], path: str):
        self._d = data
        self.path = path

    # -- meta ------------------------------------------------------------------
    @property
    def meta(self) -> Dict[str, Any]:
        return self._d["meta"]

    @property
    def seed(self) -> int:
        return int(self._d["meta"]["seed"])

    # -- CQAs ------------------------------------------------------------------
    @property
    def cqas(self) -> List[Dict[str, Any]]:
        return self._d["cqas"]

    def cqa(self, key: str) -> Dict[str, Any]:
        for c in self._d["cqas"]:
            if c["key"] == key:
                return c
        raise KeyError(f"no CQA {key!r}")

    # -- in-process acceptance criteria ----------------------------------------
    @property
    def ipc_limits(self) -> Dict[str, Any]:
        """In-process acceptance criteria: the limit each step's own output must meet.

        The criteria in ``cqas`` are drug-substance criteria and are the wrong yardstick for
        an intermediate. Every entry here is a rule evaluated against the seeded outputs (a
        backward calculation through the clearance chain, a capability alert limit, or a
        modular clearance claim), never a literal number, so the limits move with the seed.
        Returns ``{}`` when the block is absent, so an older config still loads."""
        return self._d.get("ipc_limits", {})

    # -- process ---------------------------------------------------------------
    @property
    def process(self) -> Dict[str, Any]:
        return self._d["process"]

    def unit_op(self, key: str) -> UnitOpConfig:
        raw = self._d["process"][key]
        params = [
            Parameter(
                key=p["key"], name=p["name"], unit=p.get("unit", ""),
                setpoint=p.get("setpoint", 0.0), classification=p.get("classification", ""),
                study=p.get("study", ""), prange=list(p.get("range", [0, 0])),
                nor=list(p.get("nor", p.get("range", [0, 0]))),
            )
            for p in raw.get("parameters", [])
        ]
        return UnitOpConfig(key=key, step=raw.get("step", 0), name=raw["name"],
                            parameters=params, raw=raw)

    @property
    def train_order(self) -> List[str]:
        """Unit-operation keys in processing order."""
        return sorted(self._d["process"], key=lambda k: self._d["process"][k].get("step", 99))

    # -- risk ------------------------------------------------------------------
    @property
    def risk(self) -> Dict[str, Any]:
        return self._d["risk"]

    def raw(self) -> Dict[str, Any]:
        return self._d


@lru_cache(maxsize=4)
def load_config(path: str = _DEFAULT_CFG) -> Config:
    with open(path) as fh:
        data = yaml.safe_load(fh)
    return Config(data, path)
