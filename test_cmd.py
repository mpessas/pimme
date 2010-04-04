# -*- coding: utf-8 -*-

import os
import unittest
import secret_key
import settings
settings.read_settings(None)
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

    def value_from_clipboard(self):
        if settings.dbus_support:
            import dbus
            bus = dbus.SessionBus()
            clipboard = bus.get_object('org.kde.klipper', '/klipper')
            content = clipboard.getClipboardContents()
            return content
        return ''

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

    def test_atag_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'atag')

    def test_atag_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'atag', 'test')

    def test_atag_success(self):
        self.cmd.cmd_add('first')
        self.assertTrue(self.cmd.cmd_atag('first', 'bank'))
        self.assertTrue('bank' in self.cmd.infocollection['first'].tags)

    def test_rtag_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'rtag')

    def test_rtag_item_not_exists(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'rtag', 'test')

    def test_rtag_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.assertTrue(self.cmd.cmd_rtag('first', 'bank'))
        self.assertFalse(len(self.cmd.infocollection['first'].tags))

    def test_list_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'list')

    def test_list_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.cmd.cmd_add('second', 'personal')
        self.assertEqual(len(self.cmd.cmd_list('bank')), 1)

    def test_print_item_does_not_exist(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'print', 'test')

    def test_print_item_success(self):
        self.cmd.cmd_add('first')
        self.assertTrue(self.cmd.cmd_print('first'))

    def test_show_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'show')

    def test_show_item_does_not_exist(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'show', 'test')

    def test_show_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.cmd.cmd_add('second', 'personal')
        self.assertEqual(self.cmd.cmd_show('first'), settings.value)

    def test_copy_not_enough_args(self):
        self.assertRaises(TypeError, self.cmd, 'copy')

    def test_copy_item_does_not_exist(self):
        self.assertRaises(pim_errors.ItemDoesNotExistError,
                          self.cmd, 'copy', 'test')

    def test_copy_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.cmd.cmd_add('second', 'personal')
        self.cmd.cmd_copy('first')
        content = self.value_from_clipboard()
        self.assertEqual(content, settings.value)

    def test_default_copy_success(self):
        self.cmd.cmd_add('first', 'bank')
        self.cmd.cmd_add('second', 'personal')
        self.cmd.__call__('first')
        content = self.value_from_clipboard()
        self.assertEqual(content, settings.value)

    def test_commands(self):
        self.assertEqual(len(self.cmd.cmd_commands()), 9)

if __name__ == '__main__':
    unittest.main()
