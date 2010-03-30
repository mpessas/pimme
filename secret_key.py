# -*- coding: utf-8 -*-

"""
Functions to obtain the secret key.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import sys
import getpass
import optparse
import keyring.core

__version__ = 0.1

def set_key_to_keyring(username=None, password=None):
    """Store the given password to keyring service.

    If password is None, ask the user for one.
    """
    if username is None:
        # We do not care for the "correct" username,
        # so just use getpass instead of geteuid
        username = getpass.getuser()
    if password is None:
        password = getpass.getpass()
    k = keyring.core.get_keyring()
    k.set_password(u'pim', username, password)
        
def get_key_from_keyring(username=None):
    if username is None:
        # We do not care for the "correct" username,
        # so just use getpass instead of geteuid
        username = getpass.getuser() 
    k = keyring.core.get_keyring()
    return k.get_password('pim', username)

def get_key_from_user():
    return getpass.getpass()

def get_key_dummy():
    return u'12345678'

def set_cmd_options():
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser()
    parser.add_option('-s', '--set', dest='set', action='store_true',
                      default=False, help='Store password to keyboard')
    parser.add_option('-u', '--username', dest='username',
                      help='Username')
    parser.add_option('-p', '--password', dest='password',
                      help='New password')
    return parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = set_cmd_options()
    (options, args) = parser.parse_args(argv)

    if options.set:
        username = options.username or getpass.getuser()
        password = options.password or getpass.getpass()
        set_key_to_keyring(username, password)
        return 0

if __name__ == '__main__':
    sys.exit(main())
