from typing import TypeVar

from PyQt6.QtWidgets import QWidget, QPushButton

from codiet.views.dialogs.icon_message_buttons_dialog_view import IconMessageButtonsDialogView
from codiet.controllers.dialogs.icon_message_dialog import IconMessageDialog

T = TypeVar('T', bound=IconMessageButtonsDialogView)

class IconMessageButtonsDialog(IconMessageDialog[T]):
    """A dialog box with an icon, a message and a set of buttons.
    Extends IconMessageDialog to add buttons.
    """

    def __init__(
            self,
            buttons: list[QPushButton]|None = None,
            *args, **kwargs
    ):
        self._buttons = buttons
        super().__init__(*args, **kwargs)

    def _create_view(self, parent: QWidget, *args, **kwargs) -> IconMessageButtonsDialogView:
        return IconMessageButtonsDialogView(
            parent=parent, 
            buttons=self._buttons,
            *args, **kwargs
        )
