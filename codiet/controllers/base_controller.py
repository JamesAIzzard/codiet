import logging
from typing import Type, TypeVar, Generic
from abc import ABC

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

T = TypeVar('T')
logger = logging.getLogger(__name__)

class ControllerMeta(type(QObject), ABC.__class__):
    pass

class BaseController(QObject, Generic[T], metaclass=ControllerMeta):
    """Base controller class for all controllers in the application."""

    def __init__(
        self,
        view_type: Type[T],
        parent: QWidget|None = None,
        view: T|None = None,
        *args, **kwargs
    ):
        if view is None and parent is None:
            raise ValueError("Either a view or a parent must be provided")

        if view is not None and parent is not None:
            logger.warning(
                "Both view and parent were provided to BaseController. "
                "This may lead to unexpected behavior. Consider passing only one."
            )

        super().__init__(parent=parent)
        
        self._view: T = view if view is not None else self._create_view(view_type, parent, *args, **kwargs)

    def _create_view(self, view_type: Type[T], parent: QWidget|None, *args, **kwargs) -> T:
        """Create a new view instance."""
        return view_type(parent=parent, *args, **kwargs)  # type: ignore

    @property
    def view(self) -> T:
        """Get or set the view associated with this controller."""
        return self._view

    @view.setter
    def view(self, new_view: T):
        self._view = new_view