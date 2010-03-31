# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os.path
import secret_key

get_key = secret_key.get_key_from_keyring
config_file = os.path.expanduser('~/.pimme')
