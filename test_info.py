# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import os
import unittest
import tempfile
import json
import secret_key
import settings
settings.get_key = secret_key.get_key_dummy
settings.data_file = '/tmp/rm.txt'
import crypto
import info


class TestEncryption(unittest.TestCase):

    def test_encryption(self):
        class Test(object):
            enc = crypto.EncryptedDescriptor()
        t = Test()
        data = u'1234567890'
        t.enc = data
        self.assertEqual(t.enc, data)


class TestInfoItem(unittest.TestCase):

    def setUp(self):
        self.value = u'value'

    def test_enc_getter(self):
        c = crypto.Cipher(secret_key.get_key_dummy())
        e = c.encrypt(self.value)
        i = info.InfoItem(u'name', e)
        self.assertEqual(self.value, i.value)

    def test_enc_setter(self):
        c = crypto.Cipher(secret_key.get_key_dummy())
        e = c.encrypt(u'dummy')
        i = info.InfoItem(u'name', e)
        i.value = self.value
        self.assertEqual(self.value, i.value)


class TestJSON(unittest.TestCase):

    def setUp(self):
        value = u'value'
        c = crypto.Cipher(secret_key.get_key_dummy())
        e = c.encrypt(value)
        self.item = info.InfoItem(u'name', e)

    def test_encoding(self):
        json_msg = json.dumps(self.item, cls=info.InfoItemEncoder)
        msg = json.loads(json_msg, object_hook=info.infoitem_decoder)
        self.assertEqual(msg, self.item)


class TestInfoCollection(unittest.TestCase):
    def setUp(self):
        self.col = info.InfoCollection()
        self.item = info.InfoItem('name', None)
        self.item.value = 'value'
        self.item_with_tags = info.InfoItem('tagged')
        self.item_with_tags.value = '12345667dsds'
        self.item_with_tags.tags = set(['bank', 'password', 'travel'])

    def tearDown(self):
        if os.path.exists(settings.data_file):
            os.unlink(settings.data_file)

    def test_save(self):
        self.col.load()
        self.col.add(self.item)
        self.col.save()
        item_in_json = json.dumps(self.item, cls=info.InfoItemEncoder)
        with open(settings.data_file) as f:
            line = f.readline()
            line = line[:-1]
            self.assertEqual(line, item_in_json)

    def test_load(self):
        item_in_json = json.dumps(self.item, cls=info.InfoItemEncoder)
        with open(settings.data_file, 'w') as f:
            f.write(item_in_json + '\n')
        self.col.load()
        self.assertEqual(self.col[self.item.name], self.item)

    def test_add(self):
        self.col.load()
        self.col.add(self.item)
        self.assertEqual(len(self.col), 1)

    def test_getitem(self):
        self.col.load()
        self.col.add(self.item)
        self.assertEqual(self.col[self.item.name], self.item)

    def test_search(self):
        self.col.load()
        item = info.InfoItem('account')
        item.value='0x1234 09909 213243'
        item.tags = set(['bank'])
        self.col.add(item)
        self.col.add(self.item)
        self.col.add(self.item_with_tags)
        banked = self.col.search('bank')
        self.assertEqual(len(banked), 2)
        self.assertTrue(banked[0].has_tag('bank'))
        self.assertTrue(banked[1].has_tag('bank'))
        self.assertNotEqual(banked[0], banked[1])
        

if __name__ == '__main__':
    unittest.main()
