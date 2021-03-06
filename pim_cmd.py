# -*- coding: utf-8 -*-

import getpass
import settings
try:
    import dbus
except ImportError, e:
    settings.dbus_support = False
import info
import pim_errors


class PimCmd(object):
    """Class to handle command line arguments."""

    def __init__(self):
        self.cmd = {}
        self.infocollection = info.InfoCollection()
        self.infocollection.load()

    def __call__(self, name, *params):
        # First try if user entered command. Then, name of infoitem.
        if hasattr(self, 'cmd_' + name):
            getattr(self, 'cmd_' + name)(*params)
        elif name in self.infocollection:
            if settings.debug:
                print 'Not such command. Trying item instead.'
            self.cmd_copy(name, *params)
        else:
            msg = name + ': invalid command.'
            raise pim_errors.InvalidCommandError(msg)

    def cmd_add(self, name, *args):
        """Add a new item."""
        tags = set(args) or set()
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        # unless we test
        value = settings.test and settings.value or getpass.getpass('Value: ')
        item = info.InfoItem(name)
        item.value = value
        item.tags = tags
        self.infocollection.add(item)
        self.infocollection.save()
        return True

    def cmd_atag(self, name, *args):
        """Add a tag to an item."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        map(item.tags.add, args)
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_copy(self, name):
        """Copy the value of name to clipboard."""
        if not settings.dbus_support:
            msg = 'Dbus support is needed for copy.'
            raise pim_errors.CommandNotSupportedError(msg)
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        _copy_to_clipboard(item.value)
        return True

    def cmd_commands(self):
        """List available commands."""
        ops = ((getattr(self, op).__name__[4:] + ':\t\t' +
                getattr(self, op).__doc__ + '\n')
               for op in dir(self) if op.startswith('cmd_'))
        import sys
        if settings.test:
            return list(ops)
        map(sys.stdout.write, ops)

    def cmd_edit(self, name):
        """Edit an item's password."""
        # ask value from user instead of using an argument
        # so as not to have it in shell history
        # unless we test
        value = settings.test and settings.value or getpass.getpass('Value: ')
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        item.value = value
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_list(self, tag):
        """List items having a tag."""
        res = self.infocollection.search(tag)
        if settings.test:
            return list(res)
        for r in res:
            print r.name
        return True

    def cmd_print(self, name):
        """Print an item to stdout."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        if settings.test:
            return 1
        print unicode(item)
        return True

    def cmd_rtag(self, name, *args):
        """Remove a tag from an item."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        map(item.tags.remove, args)
        self.infocollection.edit(item)
        self.infocollection.save()
        return True

    def cmd_show(self, name):
        """Show the value of name."""
        if name not in self.infocollection:
            raise pim_errors.ItemDoesNotExistError
        item = self.infocollection[name]
        if settings.test:
            return item.value
        print item.value
        return True


def _copy_to_clipboard(value):
    """Copy value to clipboard.

    Uses dbus and klipper.
    """
    bus = dbus.SessionBus()
    clipboard = bus.get_object('org.kde.klipper', '/klipper')
    clipboard.setClipboardContents(value)
