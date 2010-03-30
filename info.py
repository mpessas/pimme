# -*- coding: utf-8 -*-

"""
Classes for the information stored.

@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import json
import base64
import os.path
from crypto import EncryptedDescriptor
from secret_key import get_key_from_keyring as get_key
from pim_errors import ItemExistsError, ItemDoesNotExistError

class InfoItem(object):
    """Class for items of information.

    Each item has at least an encrypted value and a name.
    Possibly, other attributes as well.
    """
    value = EncryptedDescriptor(get_key)

    def __init__(self, name, value=None, **kwargs):
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
            dic['value'] = base64.b64encode(obj._value)
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
        self.__items = {}
        self.filename = filename

    def load(self, filename=None):
        """Load PIM items from filename.

        There has to be one item per line.
        """
        if filename is None:
            filename = self.filename
        # if filename does not exist, just use the empty dict
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    item = json.loads(line, object_hook=infoitem_decoder)
                    self.__items[item.name] = item

    def save(self, filename=None):
        """Save PIM items to filename.

        One item per line is saved.
        """
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            for item in self.__items.values():
                json.dump(item, f, cls=InfoItemEncoder)
                f.write('\n')

    def add(self, item):
        """Add a PIM item to collection."""
        if self.__items.has_key(item.name):
            msg = u'The specified item already exists! Use edit?'
            raise ItemExistsError(msg)
        self.__items[item.name] = item

    def edit(self, item):
        """Edit an existing PIM item.

        Replaces current one.
        """
        if not self.__items.has_key(item.name):
            msg = u'The specified item does not exist! Use add?'
            raise ItemDoesNotExistError(msg)
        self.__items[item.name] = item

    def search(self, tag):
        """Search for infoitems with the specified tag.

        Return a list with mathing infoitems.
        """
        res = []
        for key in self.infocollection.keys():
            if tag in self.infocollection[key].tags:
                res.append(self.infocollection[key])
        return res

    def get(self, name):
        """Return an infoitem with the specified name."""
        return self.infocollection[name]
