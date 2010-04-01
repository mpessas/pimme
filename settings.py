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


def populate_default_options():
    default_options = {}
    default_options['keyring'] = 'user'
    default_options['algorithm'] = 'Blowfish'
    return default_options


def write_default_settings():
    config = ConfigParser.RawConfigParser()
    config.add_section('Cryptography')
    config.set('Cryptography', 'keyring', 'keyring')
    config.set('Cryptography', 'algorithm', 'Blowfish')
    with open(config_file, 'wb') as f:
        config.write(f)


data_file = os.path.expanduser('~/.pimme')
config_file = os.path.expanduser('~/.pimme.conf')
test = False

default_options = populate_default_options()
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
        write_default_settings()
