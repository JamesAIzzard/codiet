import typing

from PyQt6.QtWidgets import QLineEdit

import app

class CodietLineEdit(QLineEdit):
    """Extends the QLineEdit"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def text(self) -> typing.Optional[str]:
        """Extends the text method to return None if empty."""
        # If the string is empty
        if super().text().replace(" ", "") == "":
            # Return None instead of string
            return None
        # Otherwise, just return string
        else:
            return super().text()


class CodietNumberLineEdit(CodietLineEdit):
    """Custom line edit class for numerical values only."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(app.NumericalValidator())

    def text(self) -> typing.Optional[float]:
        """Returns the numerical value, or None if empty."""
        text = super().text()
        # If we got a non-None value, cast as float
        if text is not None:
            return float(text)
        # Return
        return text

