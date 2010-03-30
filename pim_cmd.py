# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os.path
import getpass
import info


class PimCmd(object):
    """Class to handle command line arguments."""

    def __init__(self):
        self.cmd = {}
        self.__populate_cmd()
        filename = os.path.expanduser('~/.pimme')
        self.infocollection = info.InfoCollection(filename)
        self.infocollection.load()

    def __populate_cmd(self):
        self.cmd['add'] = self.add
        self.cmd['edit'] = self.edit
        self.cmd['add_tag'] = self.add_tag

    def add(self, args):
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

    def edit(self, args):
        """Edit an infoitem's password."""
        name = args[0]
        value = getpass.getpass()
        item = self.infocollection.get(name)
        item.value = value
        self.edit(item)
        self.infocollection.save()

    def add_tag(self, args):
        """Add a tag to an infoitem."""
        name = args[0]
