from contextlib import contextmanager

from PyQt6.QtWidgets import QWidget

@contextmanager
def block_signals(widget: QWidget):
    old_state = widget.blockSignals(True)  # Block signals and save the old state
    try:
        yield
    finally:
        widget.blockSignals(old_state)  # Restore the original signal blocking state