# -*- coding: utf-8 -*-
"""Non-graphical part of the Table step in a MolSSI workflow"""

import logging
import molssi_workflow
from molssi_workflow import units, Q_, data  # nopep8
import table_step
import pandas

logger = logging.getLogger(__name__)
methods = ['create', 'read', 'save', 'print', 'add row']


class Table(molssi_workflow.Node):
    def __init__(self,
                 workflow=None,
                 extension=None):
        '''Setup the non-graphical part of the Table step in a
        MolSSI workflow.

        Keyword arguments:
        '''
        logger.debug('Creating Table {}'.format(self))

        self._method = 'create'
        self.name = 'table1'
        self.column_names = []
        self.filename = ''

        super().__init__(
            workflow=workflow,
            title='Table',
            extension=extension)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        if value in table_step.methods:
            self._method = value
        else:
            raise RuntimeError('The table method must one of ' +
                               ', '.join(table_step.methods) +
                               'not "' + value + '"')

    def run(self):
        """Run a Table step.
        """
        if self.method == 'create':
            pass
        elif self.method == 'read':
            logger.debug('  read table from {}'.format(self.filename))
            table = pandas.read_csv(self.filename)
            logger.debug('  setting up dict in {}'.format(self.name))
            # tmp['type'] = 'pandas'
            # tmp['table'] = table
            # tmp['filename'] = self.filename
            molssi_workflow.workflow_variables[self.name] = {
                'type': 'pandas',
                'filename': self.filename,
                'table': table
            }
            logger.info('Succesfully read table from {}'.format(self.filename))
        elif self.method == 'save':
            raise RuntimeError("Table 'save' not implemented yet")
        elif self.method == 'print':
            print("Table '{}':".format(self.name))
            print(molssi_workflow.workflow_variables[self.name]['table'])
        elif self.method == 'add row':
            raise RuntimeError("Table 'add row' not implemented yet")
        else:
            raise RuntimeError('The table method must be one of ' +
                               ', '.join(table_step.methods) +
                               'not "' + self.method + '"')

        return super().run()
