# -*- coding: utf-8 -*-

"""Non-graphical part of the Table step in SEAMM"""

import logging
from pathlib import Path, PurePath

import numpy as np
import pandas
from tabulate import tabulate

import seamm
import seamm_util.printing as printing
from seamm_util import ureg, Q_, units_class  # noqa: F401
import table_step

logger = logging.getLogger(__name__)


def column_type(dtype):
    """The table step's type for a column, given its pandas dtype.

    Text columns are "object" in pandas 2 but a string dtype in pandas 3, so test
    the kind of dtype rather than its name.

    Parameters
    ----------
    dtype : pandas or numpy dtype
        The dtype of the column.

    Returns
    -------
    str or None
        "boolean", "integer", "float" or "string"; None for any other dtype.
    """
    if pandas.api.types.is_bool_dtype(dtype):
        return "boolean"
    if pandas.api.types.is_integer_dtype(dtype):
        return "integer"
    if pandas.api.types.is_float_dtype(dtype):
        return "float"
    if pandas.api.types.is_string_dtype(dtype) or pandas.api.types.is_object_dtype(
        dtype
    ):
        return "string"
    return None


job = printing.getPrinter()
printer = printing.getPrinter("table")


class Table(seamm.Node):
    def __init__(self, flowchart=None, extension=None):
        """Setup the non-graphical part of the Table step in SEAMM.

        Keyword arguments:
        """
        logger.debug("Creating Table {}".format(self))

        # Initialize our parent class
        super().__init__(
            flowchart=flowchart, title="Table", extension=extension, logger=logger
        )

        # This needs to be after initializing subclasses...
        self.parameters = table_step.TableParameters()
        self.calls = 0

    @property
    def version(self):
        """The semantic version of this module."""
        return table_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return table_step.__git_revision__

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

        method = P["method"]
        tablename = P["table name"]
        lines = [self.header]
        lines.append(f"    {method} table '{tablename}'")

        if method == "Create":
            table = {"Column": [], "Type": [], "Default": []}
            for d in self.parameters["columns"].value:
                try:
                    table["Column"].append(self.get_value(d["name"]))
                except Exception:
                    table["Column"].append(d["name"])
                table["Type"].append(d["type"])
                if d["default"] == "":
                    table["Default"].append("")
                else:
                    try:
                        table["Default"].append(self.get_value(d["default"]))
                    except Exception:
                        table["Default"].append(d["default"])
            for tmp in tabulate(table, headers="keys", tablefmt="grid").splitlines():
                lines.append(8 * " " + tmp)
        elif method == "Read":
            filename = P["filename"]
            file_type = P["file type"]
            if file_type == "from extension":
                if isinstance(filename, str) and self.is_expr(filename):
                    lines.append(
                        f"        File: from variable '{filename}' with type from the "
                        "extension"
                    )
                else:
                    file_type = PurePath(filename).suffix
                    if file_type not in self.parameters["file type"].enumeration:
                        types = "', '".join(self.parameters["file type"].enumeration)
                        raise RuntimeError(
                            f"Cannot handle files of type '{file_type}' when reading "
                            f"table '{tablename}'.\nKnown types: '{types}'"
                        )
                    lines.append(
                        f"         File: '{filename}' with type '{file_type}' from the "
                        "extension."
                    )
            else:
                lines.append(f"         File: '{filename}' with type '{file_type}'")
        elif method == "Save":
            pass
        elif method == "Save as":
            filename = P["filename"]
            file_type = P["file type"]
            if file_type == "from extension":
                file_type = PurePath(filename).suffix
                if file_type not in self.parameters["file type"].enumeration:
                    types = "', '".join(self.parameters["file type"].enumeration)
                    raise RuntimeError(
                        f"Cannot handle files of type '{file_type}' when reading "
                        f"table '{tablename}'.\nKnown types: '{types}'"
                    )
                lines.append(
                    f"         File: '{filename}' with type '{file_type}' from the "
                    "extension."
                )
            else:
                lines.append(f"         File: '{filename}' with type '{file_type}'")
        elif method == "Print":
            pass
        elif method == "Print the current row of":
            pass
        elif method == "Append a row to":
            table = {"Column": [], "Value": []}
            for d in self.parameters["columns"].value:
                try:
                    table["Column"].append(self.get_value(d["name"]))
                except Exception:
                    table["Column"].append(d["name"])
                try:
                    table["Value"].append(self.get_value(d["value"]))
                except Exception:
                    table["Value"].append(d["value"])
            for tmp in tabulate(table, headers="keys", tablefmt="grid").splitlines():
                lines.append(8 * " " + tmp)
        elif method == "Go to the next row of":
            pass
        elif method == "Add columns to":
            table = {"Column": [], "Type": [], "Default": []}
            for d in self.parameters["columns"].value:
                try:
                    table["Column"].append(self.get_value(d["name"]))
                except Exception:
                    table["Column"].append(d["name"])
                table["Type"].append(d["type"])
                if d["type"] == "boolean":
                    if d["default"] == "":
                        default = False
                    else:
                        default = bool(d["default"])
                elif d["type"] == "integer":
                    if d["default"] == "":
                        default = 0
                    else:
                        default = int(d["default"])
                elif d["type"] == "float":
                    if d["default"] == "":
                        default = np.nan
                    else:
                        default = float(d["default"])
                elif d["type"] == "string":
                    default = d["default"]
                table["Default"].append(default)
            for tmp in tabulate(table, headers="keys", tablefmt="grid").splitlines():
                lines.append(8 * " " + tmp)
        elif method == "Get element of":
            if P["column"] == "":
                raise RuntimeError("Table get element: the column must be given")
            column = P["column"]
            if P["row"] == "":
                raise RuntimeError("Table get element: the row must be given")
            row = P["row"]
            lines.append(f"        row {row}, column {column}")
        elif method == "Set element of":
            if P["column"] == "":
                raise RuntimeError("Table set element: the column must be given")
            column = P["column"]
            if P["row"] == "":
                raise RuntimeError("Table set element: the row must be given")
            row = P["row"]
            value = P["value"]
            lines.append(f"        row {row}, column {column} = {value}")
        else:
            methods = ", ".join(table_step.methods)
            raise RuntimeError(
                f"The table method must be one of {methods}, not {method}."
            )

        return "\n".join(lines)

    def run(self):
        """Do what we need for the table, as dictated by the 'method'"""

        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )
        tablename = P["table name"]

        # Pathnames are relative to current working directory
        wd = Path(self.directory).parent

        # Print out header to the main output
        printer.important(self.description_text(P))
        printer.important("")

        system_db = self.get_variable("_system_db")

        if P["method"] == "Create":
            columns = []
            for d in self.parameters["columns"].value:
                column_name = self.get_value(d["name"])
                if any(column_name == c[0] for c in columns):
                    continue
                columns.append((column_name, d["type"], self._default(d)))

            self.logger.info(f"Creating table '{tablename}'")

            index = P["index column"]
            if index == "" or index == "--none--":
                index = None
            table = seamm.Table.create(
                system_db, tablename, columns=columns, index_column=index
            )
            self.set_variable(tablename, table)
        elif P["method"] == "Read":
            filename = P["filename"]

            self.logger.debug("  read table from {}".format(filename))

            file_type = P["file type"]
            if file_type == "from extension":
                file_type = PurePath(filename).suffix
                if file_type not in self.parameters["file type"].enumeration:
                    types = "', '".join(self.parameters["file type"].enumeration)
                    raise RuntimeError(
                        f"Cannot handle files of type '{file_type}' when reading "
                        f"table '{tablename}'.\nKnown types: '{types}'"
                    )

            index = P["index column"]
            if index == "" or index == "--none--":
                index = None
            table = seamm.Table.read(
                system_db, tablename, filename, file_type=file_type, index_column=index
            )
            self.set_variable(tablename, table)

            self.logger.info("Successfully read table from {}".format(filename))
        elif P["method"] == "Save" or P["method"] == "Save as":
            self.calls += 1
            if self.calls % P["frequency"] == 0:
                if not self.variable_exists(tablename):
                    raise RuntimeError(
                        "Table save: table '{}' does not exist.".format(tablename)
                    )
                file_type = P["file type"]
                table = self.get_table(tablename, create=False)

                if P["method"] == "Save as":
                    filename = P["filename"].strip()
                    if filename.startswith("/"):
                        filename = str(
                            Path(self.flowchart.root_directory) / filename[1:]
                        )
                    else:
                        filename = str(wd / filename)
                else:
                    filename = table.filename
                    if filename is None:
                        if file_type == "from extension":
                            file_type = ".csv"
                        filename = str(wd / tablename) + file_type

                if file_type == "from extension":
                    file_type = PurePath(filename).suffix
                    if file_type not in self.parameters["file type"].enumeration:
                        types = "', '".join(self.parameters["file type"].enumeration)
                        raise RuntimeError(
                            f"Cannot handle files of type '{file_type}' when writing "
                            f"table '{tablename}'.\nKnown types: '{types}'"
                        )
                if file_type not in seamm.table.file_types:
                    types = "', '".join(self.parameters["file type"].enumeration)
                    raise RuntimeError(
                        f"Table save: cannot handle format '{file_type}' for file "
                        f"'{filename}'\nKnown types: '{types}'"
                    )
                table.export(filename, file_type)
        elif P["method"] == "Print":
            table = self.get_table(tablename, create=False)
            for line in table.to_string().splitlines():
                printer.normal(4 * " " + line)
            printer.normal("")

        elif P["method"] == "Print the current row of":
            table = self.get_table(tablename, create=False)
            row = table.current_row
            if row is None:
                raise RuntimeError(
                    f"Table print current row: table '{tablename}' is past its last "
                    "row."
                )
            index = table._table.position(row)
            self.logger.debug("  --> {}".format(index))
            lines = table.to_dataframe().to_string(header=True, index=True)

            self.logger.debug(lines)
            self.logger.debug("-----")

            if index == 0:
                printer.normal("\n    Table '{}':".format(tablename))
                printer.normal("\n    ".join(lines.splitlines()[0:2]))
            else:
                printer.normal(4 * " " + lines.splitlines()[index + 1])

        elif P["method"] == "Append a row to":
            if not self.variable_exists(tablename):
                raise RuntimeError(
                    "Table save: table '{}' does not exist.".format(tablename)
                )
            table = self.get_table(tablename, create=False)
            columns = table.columns

            new_row = {}
            for d in self.parameters["columns"].value:
                column_name = self.get_value(d["name"])
                value = self.get_value(d["value"])
                if column_name not in columns:
                    raise RuntimeError(
                        f"Table append a row: table '{tablename}' has no column "
                        f"'{column_name}'. The columns are: {', '.join(columns)}"
                    )
                if value == "default":
                    continue
                new_row[column_name] = self._typed(table, column_name, value)
            table.append_row(**new_row)
        elif P["method"] == "Go to the next row of":
            if not self.variable_exists(tablename):
                raise RuntimeError(
                    "Table save: table '{}' does not exist.".format(tablename)
                )
            self.get_table(tablename, create=False).next_row()

        elif P["method"] == "Add columns to":
            if not self.variable_exists(tablename):
                raise RuntimeError(
                    "Table save: table '{}' does not exist.".format(tablename)
                )
            table = self.get_table(tablename, create=False)
            for d in self.parameters["columns"].value:
                column_name = self.get_value(d["name"])
                # An existing column is left as it is.
                table.add_column(column_name, d["type"], self._default(d))
        elif P["method"] == "Get element of":
            if not self.variable_exists(tablename):
                raise RuntimeError(
                    "Table get element: table '{}' does not exist.".format(tablename)
                )
            if P["column"] == "":
                raise RuntimeError("Table get element: the column must be given")
            column = self.get_value(P["column"])
            if P["row"] == "":
                raise RuntimeError("Table get element: the row must be given")
            row = self.get_value(P["row"])
            if P["variable name"] == "":
                raise RuntimeError(
                    "Table get element: the name of the variable to "
                    "set to the value must be given"
                )
            variable_name = self.get_value(P["variable name"])

            table = self.get_table(tablename, create=False)
            row = self._row(table, row)
            column = self._column(table, column)

            value = table.get_cell(column, row)
            self.set_variable(variable_name, value)
        elif P["method"] == "Set element of":
            if not self.variable_exists(tablename):
                raise RuntimeError(
                    "Table get element: table '{}' does not exist.".format(tablename)
                )
            if P["column"] == "":
                raise RuntimeError("Table get element: the column must be given")
            column = self.get_value(P["column"])
            if P["row"] == "":
                raise RuntimeError("Table get element: the row must be given")
            row = self.get_value(P["row"])
            if P["value"] == "":
                raise RuntimeError("Table set element: the value must be given")
            value = self.get_value(P["value"])

            table = self.get_table(tablename, create=False)
            # Writing to the current row past the end of the table appends it.
            row = self._row(table, row, write=True)
            column = self._column(table, column)

            table.set_cell(column, self._typed(table, column, value), row)
        else:
            methods = ", ".join(table_step.methods)
            raise RuntimeError(
                f"The table method must be one of {methods}, not {P['method']}."
            )

        return next_node

    def _default(self, d):
        """The default value of a column defined in the dialog."""
        if d["type"] == "boolean":
            if d["default"] == "":
                return False
            return bool(d["default"])
        if d["type"] == "integer":
            if d["default"] == "":
                return 0
            return int(d["default"])
        if d["type"] == "float":
            if d["default"] == "":
                return np.nan
            return float(d["default"])
        return d["default"]

    def _typed(self, table, column, value):
        """Text from the dialog converted to the column's type, if it can be."""
        if isinstance(value, str) and table.column_type(column) in (
            "boolean",
            "integer",
            "float",
        ):
            try:
                return table.convert(column, value)
            except ValueError:
                pass
        return value

    def _row(self, table, row, write=False):
        """The table row for 'current', a position, or an index-column value.

        For a write, 'current' past the last row is None: the write appends a row.
        """
        if row == "current":
            row = table.current_row
            if row is None and not write:
                raise RuntimeError(
                    f"Table '{table.name}' has no current row: it is past the last row."
                )
            return row
        if table.index_column is None:
            return table.locate(position=int(row))
        return table.locate(key=table.convert(table.index_column, row))

    def _column(self, table, column):
        """A column given by name or by number (not counting the index column)."""
        try:
            number = int(column)
        except Exception:
            if column not in table.columns:
                raise RuntimeError(f"Table '{table.name}' has no column '{column}'.")
            return column
        columns = [c for c in table.columns if c != table.index_column]
        return columns[number]
