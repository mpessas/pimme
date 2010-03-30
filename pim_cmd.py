# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os.path
import getpass
import info

class PimCmd(object):
    def __init__(self):
        self.cmd = {}
        self.populate_cmd()
        filename = os.path.expanduser('~/.pimme')
        self.infocollection = info.InfoCollection(filename)
        self.infocollection.load()

    def populate_cmd(self):
        self.cmd['add'] = self.add
        self.cmd['edit'] = self.edit
        
    def add(self, name, tags):
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        value = getpass.getpass()
        item = info.InfoItem(name)
        item.value = value
        if tags:
            item.tags = set(tags)
        self.infocollection.add(item)
        self.infocollection.save()

    def edit(self):
        print 'Edit called'
