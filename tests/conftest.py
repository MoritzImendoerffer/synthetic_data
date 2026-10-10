"""Shared test setup."""
import pytest


@pytest.fixture(autouse=True)
def _default_table_rules(monkeypatch):
    """Every test sees the default table rules, whatever the shell exports: PC_TABLE_RULES selects
    the rules of a variant rendering pass (pc_package/ctable.py) and would change the LaTeX the
    table tests compare. A test of the variants sets it itself."""
    monkeypatch.delenv("PC_TABLE_RULES", raising=False)
