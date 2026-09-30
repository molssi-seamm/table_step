#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `table_step` running full flowcharts."""

from pathlib import Path

import pandas
import pytest
from seamm_exec import run

test_dir = Path(__file__).resolve().parent


@pytest.fixture(autouse=True)
def fresh_parsers(monkeypatch):
    """Each flowchart run registers its options on SEAMM's global argument parsers;
    start every test with none, so that two runs in one process do not conflict."""
    import seamm_util.argument_parser

    monkeypatch.setattr(seamm_util.argument_parser, "_parsers", {})


flowcharts = [
    str(test_dir / path) for path in sorted(test_dir.glob("flowcharts/*.flow"))
]


@pytest.mark.integration
@pytest.mark.parametrize("flowchart", flowcharts)
def test_flowchart(monkeypatch, tmp_path, flowchart):
    monkeypatch.setattr(
        "sys.argv",
        [
            "testing",
            flowchart,
            "--standalone",
        ],
    )

    run(wdir=str(tmp_path))


@pytest.mark.integration
def test_append_text_rows(monkeypatch, tmp_path):
    """Appending rows to a table with text columns (broken with pandas 3).

    The loop catches errors in its iterations, so check the rows themselves.
    """
    flowchart = str(test_dir / "flowcharts" / "append_text_rows.flow")
    monkeypatch.setattr("sys.argv", ["testing", flowchart, "--standalone"])

    run(wdir=str(tmp_path))

    table = pandas.read_csv(tmp_path / "rows.csv")
    assert list(table["SMILES"]) == ["C", "CC", "CCC"]
    assert list(table["n"]) == [1, 2, 3]
    assert list(table["note"]) == ["none", "none", "none"]
