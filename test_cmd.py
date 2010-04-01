# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os
import unittest
import secret_key
import settings
settings.get_key = secret_key.get_key_dummy
settings.test = True
settings.value = 'asdf1234'
settings.data_file = '/tmp/rm.txt'
import pim_errors
import pim_cmd
import info

class TestCmd(unittest.TestCase):
    def setUp(self):
        self.cmd = pim_cmd.PimCmd()

    def tearDown(self):
        if os.path.exists(settings.data_file):
            os.unlink(settings.data_file)

    def test_invalid_operation(self):
        self.assertRaises(pim_errors.InvalidCommandError,
                          self.cmd, 'nonexistent', 'param')

    def test_add_not_enough_args(self):
        self.assertRaises(pim_errors.NotEnoughArgsError
                          , self.cmd, 'add')

    def test_add_already_exists(self):
        self.cmd.add('first')
        self.assertRaises(pim_errors.ItemExistsError,
                          self.cmd, 'add', 'first')

    def test_add_success(self):
        self.assertTrue(self.cmd.add('second'))

    def test_edit_not_enough_args(self):
        self.assertRaises(pim_errors.NotEnoughArgsError,
                          self.cmd, 'edit')

    def test_edit_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'edit', 'first')

    def test_edit_item_success(self):
        self.cmd.add('first')
        self.assertTrue(self.cmd.edit('first'))

if __name__ == '__main__':
    unittest.main()
