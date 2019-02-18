# -*- coding: utf-8 -*-
"""The graphical part of a Table step"""

import molssi_workflow
import molssi_util.molssi_widgets as mw
import Pmw
import pprint  # nopep8
import table_step
import tkinter as tk
import tkinter.ttk as ttk


class TkTable(molssi_workflow.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    node_class = table_step.Table

    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 x=120, y=20, w=200, h=50):
        '''Initialize a node

        Keyword arguments:
        '''
        self.dialog = None

        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=x, y=y, w=w, h=h)

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit Table step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # self._widget, which is inherited from the base class, is
        # a place to store the pointers to the widgets so that we can access
        # them later. We'll set up a short hand 'w' just to keep lines short

        w = self._widget
        frame = ttk.Frame(self.dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)
        w['frame'] = frame

        # Set the first parameter -- which will be exactly matched
        method_label = ttk.Label(
            frame, text='Operation:'
        )
        w['method_label'] = method_label

        method = ttk.Combobox(
            frame, state='readonly',
            values=table_step.methods,
            justify=tk.RIGHT, width=15
        )
        method.set(self.node.method)
        w['method'] = method

        # Name of table
        name_label = ttk.Label(
            frame, text=' table named '
        )
        w['name_label'] = name_label

        name = ttk.Entry(frame, width=15)
        name.insert(0, self.node.name)
        w['name'] = name

        # Filename
        filename_label = ttk.Label(
            frame, text=' from file:'
        )
        w['filename_label'] = filename_label

        filename = ttk.Entry(frame, width=15)
        filename.insert(0, self.node.filename)
        w['filename'] = filename

        w['file_selector'] = ttk.Label(
            frame, text='...'
        )

        self.reset_dialog()

        w['method'].bind("<<ComboboxSelected>>", self.reset_dialog)

    def reset_dialog(self, widget=None):
        # set up our shorthand for the widgets
        w = self._widget

        # and get the method, which in this example controls
        # how the widgets are laid out.
        method = w['method'].get()

        # Remove any widgets previously packed
        frame = w['frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        w['method_label'].grid(row=row, column=0, sticky=tk.E)
        w['method'].grid(row=row, column=1, sticky=tk.EW)

        if method == 'create':
            w['name_label'].grid(row=row, column=2, sticky=tk.W)
            w['name'].grid(row=row, column=3, sticky=tk.W)
        elif method == 'read':
            w['name_label'].grid(row=row, column=2, sticky=tk.W)
            w['name'].grid(row=row, column=3, sticky=tk.W)
            row += 1
            w['filename_label'].grid(row=row, column=1, sticky=tk.W)
            w['filename'].grid(row=row, column=2, sticky=tk.W)
            w['file_selector'].grid(row=row, column=3, sticky=tk.W)
        elif method == 'save':
            raise RuntimeError("Table 'save' not implemented yet")
        elif method == 'print':
            w['name_label'].grid(row=row, column=2, sticky=tk.W)
            w['name'].grid(row=row, column=3, sticky=tk.W)
        elif method == 'add row':
            raise RuntimeError("Table 'add row' not implemented yet")
        else:
            raise RuntimeError('The table method must be one of ' +
                               ', '.join(table_step.methods) +
                               'not "' + method + '"')
        row += 1

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit...", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Table input
        """
        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):
        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result))

        self.dialog.deactivate(result)

        # set up our shorthand for the widgets
        w = self._widget
        # and get the method, which in this example tells
        # whether to use the value ditrectly or get it from
        # a variable in the workflow

        method = w['method'].get()

        self.node.method = method
        if method == 'create':
            self.node.name = w['name'].get()
        elif method == 'read':
            self.node.name = w['name'].get()
            self.node.filename = w['filename'].get()
        elif method == 'save':
            raise RuntimeError("Table 'save' not implemented yet")
        elif method == 'print':
            self.node.name = w['name'].get()
        elif method == 'add row':
            raise RuntimeError("Table 'add row' not implemented yet")
        else:
            raise RuntimeError('The table method must be one of ' +
                               ', '.join(table_step.methods) +
                               'not "' + method + '"')

    def handle_help(self):
        """Not implemented yet ... you'll need to fill this out!"""
        print('Help!')
