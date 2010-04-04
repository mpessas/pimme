# -*- coding: utf-8 -*-

class InvalidCommandError(Exception):
    """Command is not valid."""
    pass


class ItemExistsError(Exception):
    """Specified infoitem exists already."""
    pass


class ItemDoesNotExistError(Exception):
    """Specified infoitem does not exist."""
    pass


class InvalidOptionValueError(Exception):
    """Invalid value for option in settings."""
    pass


class NotEnoughArgsError(Exception):
    """Not enough arguments given."""
    pass


class CommandNotSupportedError(Exception):
    """Specified command is not supported."""
    pass
