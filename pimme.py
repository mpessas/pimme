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
import settings
from pim_cmd import PimCmd
from pim_errors import InvalidCommandError, NotEnoughArgsError


def set_cmd_options():
    """Set the command-line options."""
    usage = u'usage: %prog cmd name [options]'
    description = u'Store PIM information for the user in encrypted form.'
    parser = optparse.OptionParser(usage=usage, description=description)
    parser.add_option('-w', '--write-settings', dest='write_settings',
                      help=u'Write default settings to configuration file.')
    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug', help='Turn debugging on')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = set_cmd_options()
    (options, args) = parser.parse_args(argv)

    if options.debug:
        settings.debug = True

    try:
        command = PimCmd()
        if len(args) == 1:
            msg = u'You have not specified a command!'
            raise InvalidCommandError(msg)
        cmd_name = args[1]
        params = args[2:]
        return command(cmd_name, *params)
    except (TypeError, NotEnoughArgsError), e:
        if settings.debug:
            print e
        print 'Not enough arguments given.'
        return -1
    except InvalidCommandError, e:
        print e, e.__doc__
        return -1
    # except IndexError, e:
    #     print 'Not enough arguments!'
    #     return -1

if __name__ == '__main__':
    sys.exit(main())
