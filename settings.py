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


config_file = os.path.expanduser('~/.pimme.conf')
test = False
value = None
debug = False
data_file = None
get_key = None
CipherAlgorithm = None
IV = None

def create_default_options():
    """Return a dict with default options set."""
    default = {}
    default['keyring'] = 'user'
    default['algorithm'] = 'Blowfish'
    return default


def write_default_settings(filename=config_file):
    """Write default settigns to filename."""
    c = ConfigParser.RawConfigParser()
    c.add_section('Cryptography')
    c.set('Cryptography', 'keyring', 'keyring')
    c.set('Cryptography', 'algorithm', 'Blowfish')
    c.add_section('General')
    c.set('General', 'data_filename', '~/.pimme')
    filename = os.path.expanduser(filename)
    with open(filename, 'wb') as f:
        c.write(f)


def read_settings(filename=config_file):
    """Read the configuration from config_file."""
    global data_file
    global get_key
    global CipherAlgorithm
    global IV
    
    default_options = create_default_options()
    config = ConfigParser.RawConfigParser(default_options)
    config.read(config_file)

    data_filename = config.get('General', 'data_filename')
    data_file = os.path.expanduser(data_filename)

    keyring = config.get('Cryptography', 'keyring')
    if  keyring == 'user':
        get_key = secret_key.get_key_from_user
    elif keyring == 'keyring':
        get_key = secret_key.get_key_from_keyring
    else:
        raise InvalidOptionValueError(u'Invalid value for "keyring"')

    alg = config.get('Cryptography', 'algorithm')
    if alg == 'Blowfish':
        CipherAlgorithm = Blowfish
        IV = 'init_val'
    elif alg == 'AES':
        CipherAlgorithm = AES
        IV = 'initial valueAES'
    else:
        raise InvalidOptionValueError(u'Invalid value for "algorithm".')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-w':
        write_default_settings(config_file)
