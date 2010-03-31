# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os.path
import getpass
import info
import pim_errors
from secret_key import get_key_from_keyring


class PimCmd(object):
    """Class to handle command line arguments."""

    def __init__(self, filename=None, pw_function=get_key_from_keyring):
        self.cmd = {}
        self.__populate_cmd()
        filename_ = filename or os.path.expanduser('~/.pimme')
        self.infocollection = info.InfoCollection(filename, pw_function)
        self.infocollection.load()

    def __call__(self, name, params):
        try:
            getattr(self, name)(params)
        except AttributeError:
            raise pim_errors.InvalidCommandError
        
    def __populate_cmd(self):
        self.cmd['add'] = self.add
        self.cmd['edit'] = self.edit
        self.cmd['add_tag'] = self.add_tag

    def add(self, *args):
        """Add a new infoitem."""
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        name = args[0]
        tags = set(args[1:]) or set()
        value = getpass.getpass()
        item = info.InfoItem(name)
        item.value = value
        item.tags = tags
        self.infocollection.add(item)
        self.infocollection.save()
        return True

    def edit(self, *args):
        """Edit an infoitem's password."""
        name = args[0]
        value = getpass.getpass()
        item = self.infocollection.get(name)
        item.value = value
        self.edit(item)
        self.infocollection.save()

    def add_tag(self, *args):
        """Add a tag to an infoitem."""
        name = args[0]
