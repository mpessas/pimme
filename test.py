# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""
import unittest
import crypto
import secret_key
import info

class TestEncryption(unittest.TestCase):
    def test_encryption(self):
        class Test(object):
            enc = crypto.EncryptedDescriptor(secret_key.get_key_dummy)
        t = Test()
        data = u'1234567890'
        t.enc = data
        self.assertEqual(t.enc, data)

class TestInfoItem(unittest.TestCase):
    def setUp(self):
        self.value = u'value'
        
    def test_enc_getter(self):
        c = crypto.Cipher(secret_key.get_key_from_keyring())
        e = c.encrypt(self.value)
        i = info.InfoItem(u'name', e)
        self.assertEqual(self.value, i.value)

    def test_enc_setter(self):
        c = crypto.Cipher(secret_key.get_key_dummy())
        e = c.encrypt(u'dummy')
        i = info.InfoItem(u'name', e)
        i.value = self.value
        self.assertEqual(self.value, i.value)
        
if __name__ == '__main__':
    unittest.main()
