# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""


class InvalidCommandError(Exception):
    """Specified command is not valid."""
    pass


class ItemExistsError(Exception):
    """Specified infoitem exists already."""
    pass


class ItemDoesNotExistError(Exception):
    """Specified infoitem does not exist."""
    pass
