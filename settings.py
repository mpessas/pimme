# -*- coding: utf-8 -*-

"""
Settings module.
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
dbus_support = True


def create_default_options():
    """Return a dict with default options set."""
    default = {}
    default['keyring'] = 'user'
    default['algorithm'] = 'Blowfish'
    return default


def write_default_settings(filename):
    """Write default settigns to filename."""
    if filename is None:
        filename = config_file
    settings = """# Settings for pimme.

[Cryptography]
# Where to get the encryption key from.
# Possible values: keyring (keyring service), user (ask user)
keyring = keyring
# Encryption algorithm to use.
# Possible values: Blowfish, AES
algorithm = Blowfish

[General]
# Where to store data.
# Give an absolute path to file.
data_filename = ~/.pimme

"""
    with open(os.path.expanduser(filename), 'w') as f:
        f.write(settings)


def read_settings(filename):
    """Read the configuration from config_file."""
    global data_file
    global get_key
    global CipherAlgorithm
    global IV

    if filename is None:
        filename = config_file
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
