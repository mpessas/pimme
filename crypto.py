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
        self.__attr = attr        

    def __get__(self, instance, owner):
        """Get the decrypted data."""
        c = Cipher(self.__key)
        return c.decrypt(getattr(instance, self.__attr))

    def __set__(self, instance, value):
        """Encrypt the value and store it."""
        c = Cipher(self.__key)
        enc = c.encrypt(value)
        setattr(instance, self.__attr, enc)

class Cipher(object):
    """Class to encrypt and decrypt values."""
    
    def __init__(self, key, padding_char='\x00'):
        self.__key = key
        self.__padding_char = padding_char

    def encrypt(self, value):
        """Encrypt the parameter.

        Use padding, if the parameter does not have
        the necessary length.
        """
        padded = self.__pad(value)
        cipher = self.__cipher()
        return cipher.encrypt(padded)

    def decrypt(self, enc):
        """Decrypt the parameter.

        Return the value after removing the padding characters.
        """
        cipher = self.__cipher()
        value = cipher.decrypt(enc)
        return self.__depad(value)
        
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
