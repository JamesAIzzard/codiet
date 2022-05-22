import typing

from PyQt6 import QtGui

class PositiveFloatValidator(QtGui.QValidator):
    def validate(self, input: str, pos: int) -> typing.Tuple[QtGui.QValidator.State, str, int]:
        # Allow empty string
        if input == "":
            return (QtGui.QValidator.State.Intermediate, input, pos)
        # Start by trying to convert text to float
        try:
            value = float(input)
        except ValueError:
            return (QtGui.QValidator.State.Invalid, input, pos)
        # Now check float is greater than zero
        if value < 0:
            return (QtGui.QValidator.State.Invalid, input, pos)
        # All OK, return valid
        return (QtGui.QValidator.State.Acceptable, input, pos)

class Float0To100Validator(QtGui.QValidator):
    def validate(self, input: str, pos: int) -> typing.Tuple[QtGui.QValidator.State, str, int]:
        # Allow empty string
        if input == "":
            return (QtGui.QValidator.State.Intermediate, input, pos)
        # Start by trying to convert text to float
        try:
            value = float(input)
        except ValueError:
            return (QtGui.QValidator.State.Invalid, input, pos)
        # Now check float is greater than zero
        if value < 0 or value > 100:
            return (QtGui.QValidator.State.Invalid, input, pos)
        # All OK, return valid
        return (QtGui.QValidator.State.Acceptable, input, pos)        
        