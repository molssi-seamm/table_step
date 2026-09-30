#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `table_step` package."""

import pytest
import table_step  # noqa: F401


def test_construction():
    """Simplest test that we can make a Table object"""
    table = table_step.Table()
    assert str(type(table)) == "<class 'table_step.table.Table'>"


@pytest.mark.parametrize(
    "values, dtype, expected",
    [
        (["a", "b"], None, "string"),  # object in pandas 2, a string dtype in 3
        (["a", "b"], "object", "string"),
        (["a", "b"], "string", "string"),
        ([True, False], None, "boolean"),
        ([1, 2], None, "integer"),
        ([1, 2], "Int32", "integer"),
        ([1.5, 2.0], None, "float"),
        (["2026-09-30"], "datetime64[ns]", None),
    ],
)
def test_column_type(values, dtype, expected):
    """The table's column types, whatever pandas calls the dtype."""
    import pandas

    column = pandas.Series(values, dtype=dtype)
    assert table_step.table.column_type(column.dtype) == expected


def test_column_type_of_empty_text_column():
    """An empty text column, as 'Create' makes it."""
    import pandas

    table = pandas.DataFrame()
    table["SMILES"] = pandas.Series([], dtype=str)
    assert table_step.table.column_type(table.dtypes["SMILES"]) == "string"
