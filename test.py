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
    def test_descriptor(self):
        value = u'value'
        c = crypto.cipher('1234')
        e = c.encrypt(crypto.pad(value, '\x00'))
        i = info.InfoItem(u'name', e)
        self.assertEqual(value, i.value)
        
if __name__ == '__main__':
    unittest.main()
