import typing

from PyQt6 import QtGui

class NumericalValidator(QtGui.QValidator):
    def validate(self, input:str, pos: int) -> typing.Tuple[QtGui.QValidator.State, str, int]:
        # Allow empty string
        if input == "":
            return (QtGui.QValidator.State.Intermediate, input, pos)
        # Try and convert text to float
        try:
            value = float(input)
        except ValueError:
            return (QtGui.QValidator.State.Invalid, input, pos)
        # All OK, return valid
        return (QtGui.QValidator.State.Acceptable, input, pos)        

class PositiveFloatValidator(NumericalValidator):
    def validate(self, input: str, pos: int) -> typing.Tuple[QtGui.QValidator.State, str, int]:
        state, input, pos = super().validate(input, pos)
        if state in (QtGui.QValidator.State.Invalid, QtGui.QValidator.State.Intermediate):
            return (state, input, pos)
        # Now check float is greater than zero
        if float(input) < 0: # type: ignore
            return (QtGui.QValidator.State.Invalid, input, pos)
        # All OK, return valid
        return (QtGui.QValidator.State.Acceptable, input, pos)

class Float0To100Validator(PositiveFloatValidator):
    def validate(self, input: str, pos: int) -> typing.Tuple[QtGui.QValidator.State, str, int]:
        state, input, pos = super().validate(input, pos)
        if state in (QtGui.QValidator.State.Invalid, QtGui.QValidator.State.Intermediate):
            return (state, input, pos)
        # Now check float is greater than zero
        if float(input) < 0 or float(input) > 100: # type: ignore
            return (QtGui.QValidator.State.Invalid, input, pos)
        # All OK, return valid
        return (QtGui.QValidator.State.Acceptable, input, pos)