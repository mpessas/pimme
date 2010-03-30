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
    def __init__(self, get_key, attr='_value'):
        """Use Blowfish cipher from pycrypto."""
        self.__key = get_key()
        self.__padding_char = '\x00'        
        self.__attr = attr        

    def __get__(self, instance, owner):
        """Get the decrypted data."""
        cipher = self.__cipher()
        return self.__depad(cipher.decrypt(getattr(instance, self.__attr)))

    def __set__(self, instance, value):
        """Encrypt the value and store it."""
        cipher = self.__cipher()
        padded = self.__pad(value)
        print len(value)
        print len(padded)
        enc = cipher.encrypt(padded)
        setattr(instance, self.__attr, enc)

    def __cipher(self):
        mode = CipherAlgorithm.MODE_CBC
        iv = 'init_val'
        return CipherAlgorithm.new(self.__key, mode, iv)

    def __pad(self, value):
        npad = CipherAlgorithm.block_size - (len(value) % CipherAlgorithm.block_size)
        if npad:
            value += self.__padding_char * npad
        return value

    def __depad(self, value):
        return value.rstrip(self.__padding_char)
