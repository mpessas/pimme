# -*- coding: utf-8 -*-

"""
Classes for the information stored.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

from crypto import EncryptedDescriptor
from secret_key import get_key_from_keyring as get_key

class InfoItem(object):
    """Class for items of information.

    Each item has at least an encrypted value and a name.
    Possibly, other attributes as well.
    """
    value = EncryptedDescriptor(get_key)

    def __init__(self, name, value):
        """Initializer.

        Takes two parameters: the name of the item and
        its value in encrypted form.
        """
        self.__name = name
        self.__value = value

class InfoCollection(object):
    """A collection of InfoItems."""
    def __init__(self, filename):
        """Read all items from a file.

        Items are stored in json format in the given file.
        """
        pass
