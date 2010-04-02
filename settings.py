# -*- coding: utf-8 -*-

"""
Settings module.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import sys
import os.path
import ConfigParser
from Crypto.Cipher import Blowfish, AES
import secret_key
from pim_errors import InvalidOptionValueError


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
value = None

_default_options = create_default_options()
_config = ConfigParser.RawConfigParser(_default_options)
_config.read(config_file)

_keyring = _config.get('Cryptography', 'keyring')
if  _keyring == 'user':
    get_key = secret_key.get_key_from_user
elif _keyring == 'keyring':
    get_key = secret_key.get_key_from_keyring
else:
    raise InvalidOptionValueError(u'Invalid value for "keyring"')

_alg = _config.get('Cryptography', 'algorithm')
if _alg == 'Blowfish':
    CipherAlgorithm = Blowfish
    IV = 'init_val'
elif _alg == 'AES':
    CipherAlgorithm = AES
    IV = 'initial valueAES'
else:
    raise InvalidOptionValueError(u'Invalid value for "algorithm".')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-w':
        write_default_settings(config_file)
