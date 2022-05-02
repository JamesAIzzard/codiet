import typing

import model


class BaseQuantityError(model.exceptions.PyDietModelError):
    """Base exception for the quantity module."""

    def __init__(self, subject: typing.Any = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject