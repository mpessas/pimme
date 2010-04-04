#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PIMME application.

Store PIM information in an encrypted form.
"""

__version__ = '0.2.1'

import sys
import optparse
import getpass
import settings
from pim_cmd import PimCmd
from pim_errors import InvalidCommandError, NotEnoughArgsError, \
        CommandNotSupportedError


def set_cmd_options():
    """Set the command-line options."""
    usage = u'usage: %prog cmd_name [options]'
    desc = u'Store PIM information for the user in encrypted form.\n' + \
            'Use %prog commands to get a list of supported commands.'
    version = '%prog: version ' + __version__
    parser = optparse.OptionParser(usage=usage,
                                   description=desc,
                                   version=version)
    parser.add_option('-w', '--write-settings', action='store_true',
                      default=False, dest='write_settings',
                      help=u'Write default settings to configuration file.')
    parser.add_option('-c', '--config', dest='config_file',
                      help=u'Use CONFIG_FILE for configuration')
    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug', help='Turn debugging on')
    parser.add_option('-k', '--set-key', action='store_true',
                      dest='set_key', help='Set the encryption key.')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = set_cmd_options()
    (options, args) = parser.parse_args(argv)

    if options.set_key:
        username = getpass.getuser()
        password = getpass.getpass()
        secret_key.set_key_to_keyring(username, password)
        return 0        
    
    if options.write_settings:
        settings.write_default_settings(options.config_file)
        return 0
    settings.read_settings(options.config_file)
    if options.debug:
        settings.debug = True

    try:
        command = PimCmd()
        if len(args) == 1:
            print u'You have not specified a command!'
            print u"Use 'commands' to list the available commands."
            return -1
        cmd_name = args[1]
        params = args[2:]
        return command(cmd_name, *params)
    except (TypeError, NotEnoughArgsError), e:
        if settings.debug:
            print e
        print 'Not enough arguments given.'
        return -1
    except InvalidCommandError, e:
        print e
        return -1
    except CommandNotSupportedError, e:
        print e
        return -1
    except EOFError, e:
        if settings.debug:
            print e
        return -1

if __name__ == '__main__':
    sys.exit(main())
