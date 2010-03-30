# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

class PimCmd(object):
    def __init__(self):
        self.cmd = {}
        self.populate_cmd()

    def populate_cmd(self):
        self.cmd['add'] = self.add
        self.cmd['edit'] = self.edit
        
    def add(self):
        print 'Add called'

    def edit(self):
        print 'Edit called'
