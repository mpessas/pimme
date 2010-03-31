# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os
import unittest
import pim_errors
import pim_cmd
import secret_key

class TestCmd(unittest.TestCase):
    def setUp(self):
        self.filename = '/tmp/rm.txt'
        self.cmd = pim_cmd.PimCmd(self.filename,
                                  secret_key.get_key_dummy)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.unlink(self.filename)

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
