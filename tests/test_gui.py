# -*- coding: utf-8 -*-

"""Smoke test of the Tk dialog: create it and re-lay it out for every table method.
Skipped when no display is available."""

import pytest

import table_step


@pytest.fixture()
def tk_node():
    import tkinter as tk

    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    root.withdraw()
    import Pmw
    import seamm

    Pmw.initialise(root)
    flowchart = seamm.Flowchart(namespace="org.molssi.seamm", directory=".")
    tk_flowchart = seamm.TkFlowchart(
        master=root, flowchart=flowchart, namespace="org.molssi.seamm.tk"
    )
    node = flowchart.create_node("Table")
    flowchart.add_node(node)
    plugin = tk_flowchart.plugin_manager.get("Table")
    tk_node = plugin.create_tk_node(
        tk_flowchart=tk_flowchart, node=node, canvas=tk_flowchart.canvas, x=100, y=100
    )
    yield tk_node
    root.destroy()


def test_dialog_layouts(tk_node):
    tk_node.create_dialog()
    tk_node.reset_dialog()
    for method in table_step.TableParameters.parameters["method"]["enumeration"]:
        tk_node["method"].set(method)
        tk_node.reset_dialog()


@pytest.mark.parametrize(
    "key, choice",
    [("index column", "--none--"), ("row", "current"), ("column", "current")],
)
def test_dropdowns_offer_words_not_letters(tk_node, key, choice):
    """These choices were tuple("current"), i.e. one letter per choice."""
    tk_node.create_dialog()
    values = tk_node[key].combobox.cget("values")
    assert tuple(str(v) for v in values) == (choice,)
