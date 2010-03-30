# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

from Crypto.Cipher import Blowfish as CipherAlgorithm

class EncryptedDescriptor(object):
    """A descriptor class for encrypted data.

    Handles encryption of data transparently.
    """
    def __init__(self, get_key, attr='__value'):
        """Use Blowfish cipher from pycrypto."""
        key = get_key()
        self.__cipher = CipherAlgorithm.new(key, CipherAlgorithm.MODE_CFB)
        self.__attr = attr

    def __get__(self, instance, owner):
        """Get the decrypted data."""
        return self.__cipher.decrypt(getattr(instance, '_' + owner.__name__ + self.__attr))

    def __set__(self, instance, value):
        """Encrypt the value and store it."""
        enc = self.__cipher.encrypt(value)
        setattr(instance, '_' + owner.__name__ + self.__attr, enc)
        
