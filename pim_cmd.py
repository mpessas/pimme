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

    def __call__(self, name, params):
        try:
            getattr(self, name)(params)
        except AttributeError, e:
            raise pim_errors.InvalidCommandError

    def add(self, name=None, *args):
        """Add a new item."""
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        if not name:
            raise pim_errors.NotEnoughArgsError
        tags = set(args[1:]) or set()
        value = settings.test and settings.value or getpass.getpass()
        item = info.InfoItem(name)
        item.value = value
        item.tags = tags
        self.infocollection.add(item)
        self.infocollection.save()
        return True

    def edit(self, name=None, *args):
        """Edit an item's password."""
        if not name:
            raise pim_errors.NotEnougnArgsError
        value = settings.test and settings.value or getpass.getpass()
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        item.value = value
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def add_tag(self, *args):
        """Add a tag to an item."""
        name = args[0]
        item = self.infocollection[name]
        map(item.tags.add, args[1:])

    def remove_tag(self, *args):
        """Remove a tag from an item."""
        pass

    def export(self, *args):
        """Export data to a file (unencrypted)."""
        pass

    # def import_(self, *args):
    #     """Import unencrypted data from a file."""
    #     pass

    def list(self, *args):
        """List items having a tag."""
        pass

    def operations(self):
        """List available operations."""
        return (op for op in dir(self) if not op.startswith('_'))
