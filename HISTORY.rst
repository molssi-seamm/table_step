=======
History
=======
2026.10.3 -- Tables are stored in the job's database
    * Tables are now kept in the job's database (with seamm 2026.10.3), so a job's
      tables are saved with it even if they are never written to a file.
    * "Append a row to" works for tables with an index column; new rows get the
      columns' defaults (not empty values), and integer and boolean columns keep their
      types.
    * "Get element of" and "Set element of" work by index value for tables whose index
      column holds text, and "Set element of" the current row after going past the
      end of the table adds the row.
    * "Add columns to" uses the column name after substituting variables, and records
      the default.
    * "Go to the next row of" past the end of a table does nothing more, so it can be
      used at either end of a loop.
    * Values read with "Get element of" are plain Python numbers, not numpy ones.
2026.9.30 -- Bugfix: appending rows to tables with text columns failed with pandas 3
    * 'Append a row to' failed with an error naming the column (e.g. 'SMILES') whenever
      the table had a text column, because pandas 3 describes text columns differently
      from pandas 2. A loop over SMILES strings that appended a row each time therefore
      added no rows. It now works with both pandas 2 and 3, and appending to a column
      that the table does not have gives a clear error listing the table's columns.
    * The 'Index column', 'Row' and 'Column' dropdowns in the dialog offered single
      letters ('c', 'u', 'r', ...) instead of '--none--' or 'current'. Fixed.
    * Internal: the tests now check the rows appended in a loop, and the CI installs
      the package with uv from its declared requirements rather than a conda
      environment.

2025.6.1 -- Enhancement to allow paths with directories.
    * As in reading/writing structures, paths beginning with '/' are relative to the
      root of the job, and relative paths are relative to the directory where the table
      step is invoked.

2023.11.10 -- Bugfix: title of edit dialog was wrong

2023.10.30 -- Cleaned up output
    * Nothing large, just made the output properly indented, etc.

2023.7.25 -- Bug fix and Enhancements
    * Fixed bug with reading table using a variable for the filename, but asking for the
      type from the extension.
    * Add ability to save tables with a frequency of other than ever call.
      
2023.2.15 -- Bugs fixes and documentation
    * Restructured documentation and moved to new theme
    * Fixed bug with access rows of tables with non-integer indexes as well as "current"
      index 
    * Added support for lists of tables in pulldowns in the GUI
      
2021.12.22 -- Improved the handling of index columns, added formats.
    * Improved the handling of the index column
    * Added Save as
    * Added Excel and JSON formats.

2021.10.14 -- Updated for Python
    * Now supporting Python 3.8 and 3.9
      
2021.2.12 (12 February 2021)
----------------------------

* Updated the README file to give a better description.
* Updated the short description in setup.py to work with the new installer.
* Added keywords for better searchability.

2020.12.5 (5 December 2020)
---------------------------

* Internal: switching CI from TravisCI to GitHub Actions, and in the
  process moving documentation from ReadTheDocs to GitHub Pages where
  it is consolidated with the main SEAMM documentation.
* Updated to be compatible with the new command-line argument
  handling.

0.9 (15 April 2020)
-------------------

* General bug fixing and code cleanup.
* Part of release of all modules.

0.7.0 (17 December 2019)
------------------------

* General clean-up of code and output.
* Part of release of all modules.


0.3.0 (20 August 2019)
----------------------

* First release on PyPI.
