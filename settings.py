# -*- coding: utf-8 -*-

"""
Settings module.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os.path
import secret_key

data_file = os.path.expanduser('~/.pimme')
config_file = os.path.expanduser('~/.pimme.conf')
get_key = secret_key.get_key_from_keyring
config_file = os.path.expanduser('~/.pimme')
