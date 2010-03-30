# -*- coding: utf-8 -*-

"""
Classes for the information stored.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import json
import base64
from crypto import EncryptedDescriptor
from secret_key import get_key_from_keyring as get_key


class InfoItem(object):
    """Class for items of information.

    Each item has at least an encrypted value and a name.
    Possibly, other attributes as well.
    """
    value = EncryptedDescriptor(get_key)

    def __init__(self, name, value, **kwargs):
        """Initializer.

        Takes two parameters: the name of the item and
        its value in encrypted form. Everything else is passed
        as a dict. Currently, only 'tags' key is used.
        """
        self.name = name
        self._value = value
        self.tags = set()
        if 'tags' in kwargs:
            self.tags.update(kwargs['tags'])

    def __eq__(self, other):
        return self.name == other.name

    def __unicode__(self):
        """Return a unicode representation of object."""
        uni_s = self.name + '\n' + 'tags:\t'
        if self.tags:
            for tag in self.tags:
                uni_s += ' ' + tag
            uni_s += '\n'
        else:
            uni_s += 'None'
        return uni_s


class InfoItemEncoder(json.JSONEncoder):
    """JSON encoder for InfoItems."""

    def default(self, obj):
        """Return a serializable object fot InfoItems as well."""
        if isinstance(obj, InfoItem):
            dic = {}
            dic['name'] = obj.name
            dic['value'] = base64.b64encode(obj.value)
            dic['tags'] = list(obj.tags)
            return dic
        return super(InfoItemEncoder, self).default(obj)


def infoitem_decoder(dct):
    """Convert supplied dict to an InfoItem object."""
    name = dct['name']
    value = base64.b64decode(dct['value'])
    tags = set(dct['tags'])
    return InfoItem(name, value, tags=tags)


class InfoCollection(object):
    """A collection of InfoItems."""

    def __init__(self, filename):
        """Read all items from a file.

        Items are stored in json format in the given file.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
