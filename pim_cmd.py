# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import getpass
import info
import pim_errors
import settings


class PimCmd(object):
    """Class to handle command line arguments."""

    def __init__(self):
        self.cmd = {}
        self.infocollection = info.InfoCollection()
        self.infocollection.load()

    def __call__(self, name, *params):
        try:
            getattr(self, 'cmd_' + name)(*params)
        except AttributeError, e:
            if settings.debug:
                print e
            raise pim_errors.InvalidCommandError(name)

    def cmd_add(self, name, *args):
        """Add a new item."""
        tags = set(args) or set()
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        # unless we test
        value = settings.test and settings.value or getpass.getpass('Value: ')
        item = info.InfoItem(name)
        item.value = value
        item.tags = tags
        self.infocollection.add(item)
        self.infocollection.save()
        return True

    def cmd_edit(self, name):
        """Edit an item's password."""
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        # unless we test
        value = settings.test and settings.value or getpass.getpass('Value: ')
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        item.value = value
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_add_tag(self, name, *args):
        """Add a tag to an item."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        map(item.tags.add, args)
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_remove_tag(self, name, *args):
        """Remove a tag from an item."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        map(item.tags.remove, args)
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_list(self, tag):
        """List items having a tag."""
        res = self.infocollection.search(tag)
        if settings.test:
            return list(res)
        for r in res:
            print r.name
        return True

    def cmd_operations(self):
        """List available operations."""
        ops = ((getattr(self, op).__name__[4:] + ':\t\t' +
                getattr(self, op).__doc__ + '\n')
               for op in dir(self) if op.startswith('cmd_'))
        import sys
        if settings.test:
            return list(ops)
        map(sys.stdout.write, ops)
