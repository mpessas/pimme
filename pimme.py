#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PIMME application.

Store PIM information in an encrypted form.
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import sys
import optparse
from pim_cmd import PimCmd
from pim_errors import InvalidCommandError, NotEnoughArgsError


def set_cmd_options():
    usage = u'usage: %prog cmd name [options]'
    description = u'Store PIM information for the user in encrypted form.'
    parser = optparse.OptionParser(usage=usage, description=description)
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', help=u'Add a new item')
    parser.add_option('-c', '--config', dest='config_file',
                      help=u'Use CONFIG_FILE for configuration')
    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug', help='Turn debugging on')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = set_cmd_options()
    (options, args) = parser.parse_args(argv)

    try:
        command = PimCmd()
        if len(argv) == 1:
            msg = u'You have not specified a command!'
            raise InvalidCommandError(msg)
        cmd_name = argv[1]
        params = argv[2:]
        return command(cmd_name, params)
    except InvalidCommandError, e:
        print e.__doc__
        return -1
    except NotEnoughArgsError, e:
        print e.__doc__
        return -1
    # except KeyError, e:
    #     print u'Action ' + unicode(e) + ' is not defined!'
    #     return -1
    except IndexError, e:
        print 'Not enough arguments!'
        return -1

if __name__ == '__main__':
    sys.exit(main())
