# -*- coding: utf-8 -*-

"""
PIMME application.

Store PIM information in an encrypted form.
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import sys
import optparse

def set_cmd_options():
    usage = u'usage: %prog [options]'
    description = u'Store PIM informaition for the user in encrypted form.'
    parser = optparse.OptionParser(usage=usage, description=description)
    parser.add_option('-a', '--add', action='store_const',
                      const=0, dest='acion',
                      help=u'Add a new item.')
    parser.add_option('-i', '--item', action='store_const',
                      const=1, dest='action',
                      help=u'Edit an existing item')
    parser.add_option('-i', '--item', dest='item',
                      help=u'Edit an existing item')
    return parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = set_cmd_options()
    (options, args) = parser.parse_args(argv)

    if options.add:
        

if __name__ == '__main__':
    sys.exit(main())
