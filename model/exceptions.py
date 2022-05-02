class PyDietModelError(Exception):
    """Base exception for all exceptions raised by the model."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)