# -*- coding: utf-8 -*-

import settings


class EncryptedDescriptor(object):
    """A descriptor class for encrypted data.

    Handles encryption of data transparently.
    """

    def __init__(self, attr='_value'):
        """Use Blowfish cipher from pycrypto."""
        self.__key = None
        self.__attr = attr

    def __get__(self, instance, owner):
        """Get the decrypted data."""
        if instance is None:
            return self
        if self.__key is None:
            self.__key = self.get_key()
        cipher = Cipher(self.__key)
        return cipher.decrypt(getattr(instance, self.__attr))

    def __set__(self, instance, value):
        """Encrypt the value and store it."""
        if self.__key is None:
            self.__key = self.get_key()
        cipher = Cipher(self.__key)
        enc = cipher.encrypt(value)
        setattr(instance, self.__attr, enc)

    def get_key(self):
        """Return the encryption key.

        Use function from settings.
        """
        return settings.get_key()


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
        """Return a cipher object."""
        mode = settings.CipherAlgorithm.MODE_CBC
        return settings.CipherAlgorithm.new(self.__key, mode,
                                            settings.IV)

    def __pad(self, value):
        """Pad the value for encryption."""
        bs = settings.CipherAlgorithm.block_size
        npad = bs - (len(value) % bs)
        if npad:
            value += self.__padding_char * npad
        return value

    def __depad(self, value):
        """Remove padding from unencrypted value."""
        return value.rstrip(self.__padding_char)
