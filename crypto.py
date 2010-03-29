# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

from Crypto.Cipher import Blowfish as Cipher

class EncryptedDescriptor(object):
    """A descriptor class for encrypted data.

    Handles encryption of data transparently.
    """
    def __init__(self, get_key, attr='value'):
        """Use Blowfish cipher from pycrypto."""
        key = get_key()
        self.__cipher = new Cipher(key, Cipher.MODE_CFB)
        self.__attr = attr

    def __get__(self, instance, owner):
        """Get the decrypted data."""
        return self.__cipher.decrypt(getattr(instance, self.__attr))

    def __set__(self, instance, value):
        """Encrypt the value and store it."""
        enc = self.__cipher.encrypt(value)
        setattr(instance, self.__attr, enc)
        
