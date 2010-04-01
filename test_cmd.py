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
        self.assertRaises(TypeError, self.cmd, 'add')

    def test_add_already_exists(self):
        self.cmd.cmd_add('first')
        self.assertRaises(pim_errors.ItemExistsError,
                          self.cmd, 'add', 'first')

    def test_add_success(self):
        self.assertTrue(self.cmd.cmd_add('second'))

    def test_add_success_with_tags(self):
        self.assertTrue(self.cmd.cmd_add('second', 'tag1', 'tag2'))
        self.assertEqual(len(self.cmd.infocollection['second'].tags), 2)

    def test_edit_not_enough_args(self):
        self.assertRaises(TypeError,
                          self.cmd, 'edit')

    def test_edit_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'edit', 'first')

    def test_edit_item_success(self):
        self.cmd.cmd_add('first')
        self.assertTrue(self.cmd.cmd_edit('first'))

    def test_add_tag_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'add_tag')

    def test_add_tag_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'add_tag', 'test')

    def test_add_tag_success(self):
        self.cmd.cmd_add('first')
        self.assertTrue(self.cmd.cmd_add_tag('first', 'bank'))
        self.assertTrue('bank' in self.cmd.infocollection['first'].tags)

    def test_remove_tag_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'remove_tag')

    def test_remove_tag_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'remove_tag', 'test')

    def test_remove_tag_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.assertTrue(self.cmd.cmd_remove_tag('first', 'bank'))
        self.assertFalse(len(self.cmd.infocollection['first'].tags))

    def test_operations(self):
        self.assertEqual(len(self.cmd.cmd_operations()), 7)

if __name__ == '__main__':
    unittest.main()
