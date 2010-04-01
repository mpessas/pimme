# -*- coding: utf-8 -*-

"""
Settings module.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import sys
import os.path
import ConfigParser
import secret_key
import pim_errors


def create_default_options():
    """Return a dict with default options set."""
    default = {}
    default['keyring'] = 'user'
    default['algorithm'] = 'Blowfish'
    return default


def write_default_settings(filename):
    """Write default settigns to filename."""
    c = ConfigParser.RawConfigParser()
    c.add_section('Cryptography')
    c.set('Cryptography', 'keyring', 'keyring')
    c.set('Cryptography', 'algorithm', 'Blowfish')
    with open(filename, 'wb') as f:
        c.write(f)


data_file = os.path.expanduser('~/.pimme')
config_file = os.path.expanduser('~/.pimme.conf')
test = False

default_options = create_default_options()
config = ConfigParser.RawConfigParser(default_options)
config.read(config_file)

keyring = config.get('Cryptography', 'keyring')
if  keyring == 'user':
    get_key = secret_key.get_key_from_user
elif keyring == 'keyring':
    get_key = secret_key.get_key_from_keyring
else:
    raise pim_errors.InvalidOptionValueError(u'Invalid value for "keyring"')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-w':
        write_default_settings(config_file)
