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
settings.config_file = '/tmp/rm.txt'
import pim_errors
import pim_cmd
import info

class TestCmd(unittest.TestCase):
    def setUp(self):
        self.cmd = pim_cmd.PimCmd()

    def tearDown(self):
        if os.path.exists(settings.config_file):
            os.unlink(settings.config_file)

    def test_invalid_operation(self):
        self.assertRaises(pim_errors.InvalidCommandError,
                          self.cmd, 'nonexistent', 'param')

    def test_add_not_enough_params(self):
        self.assertRaises(TypeError, self.cmd, 'add')

    def test_add_already_exists(self):
        self.cmd.add('first')
        self.assertRaises(pim_errors.ItemExistsError,
                          self.cmd, 'add', 'first')

    def test_add_success(self):
        self.assertTrue(self.cmd.add('second'))


if __name__ == '__main__':
    unittest.main()
