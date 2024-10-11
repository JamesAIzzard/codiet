from typing import TypeVar, Generic, List, Tuple
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal

from codiet.controllers.base_controller import BaseController

T = TypeVar('T')  # Type variable for the object
V = TypeVar('V', bound=QWidget)  # Type variable for the view, constrained to QWidget

class Listbox(BaseController[QListWidget], Generic[T, V]):
    """A generic listbox controller.
    Works with a list of type T and views of type V.
    """

    itemClicked = pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init an internal pair of dictionaries to hold items and views
        self._items: dict[int, T] = {}
        self._views: dict[int, V] = {}

        # Connect signals
        self.view.itemClicked.connect(self._on_item_clicked)

    def _create_view(self, *args, **kwargs) -> QListWidget:
        return QListWidget(*args, **kwargs)

    @property
    def selected_item(self) -> T|None:
        """Get the item corresponding to the currently selected row."""
        if self.row_is_selected:
            return self._items[self.selected_index]
        return None

    @selected_item.setter
    def selected_item(self, item: T):
        """Select the row that matches the given item."""
        for index, existing_item in self._items.items():
            if existing_item == item:
                self.selected_index = index
                break

    @property
    def selected_item_view(self) -> V|None:
        """Get the view corresponding to the currently selected row."""
        if self.row_is_selected:
            return self._views[self.selected_index]
        return None

    @selected_item_view.setter
    def selected_item_view(self, view: V):
        """Select the row that matches the given view."""
        for index, existing_view in self._views.items():
            if existing_view == view:
                self.selected_index = index
                break

    @property
    def selected_index(self) -> int:
        """Get the index of the currently selected row."""
        return self.view.currentRow()

    @selected_index.setter
    def selected_index(self, index: int):
        """Select the row at the given index."""
        self.view.setCurrentRow(index)

    @property
    def row_is_selected(self) -> bool:
        """Check if a row is currently selected."""
        return self.view.currentRow() != -1

    @property
    def count(self) -> int:
        """Get the number of rows in the listbox."""
        return self.view.count()

    @property
    def items(self) -> List[T]:
        """Get a list of all items in the listbox."""
        return list(self._items.values())

    @property
    def views(self) -> List[V]:
        """Get a list of all views in the listbox."""
        return list(self._views.values())

    @property
    def items_and_views(self) -> List[Tuple[T, V]]:
        """Get a list of tuples of items and views in the listbox."""
        return [(self._items[i], self._views[i]) for i in range(self.count)]

    def add_row(self, item: T, view: V):
        """Add a row to the listbox."""
        index = self.view.count()
        list_item = QListWidgetItem(self.view)
        self.view.setItemWidget(list_item, view)
        self._items[index] = item
        self._views[index] = view

    def add_rows(self, items_and_views: List[Tuple[T, V]]):
        """Add multiple rows to the listbox."""
        for item, view in items_and_views:
            self.add_row(item, view)

    def remove_row(self, item: T|None = None, view: V|None = None):
        """Remove a row from the listbox.
        If both item and view are provided, uses view.
        """
        if item is None and view is None:
            raise ValueError("Either item or view must be provided.")
        if view is not None:
            for index, existing_view in self._views.items():
                if existing_view == view:
                    self.view.takeItem(index)
                    del self._items[index]
                    del self._views[index]
                    break
        elif item is not None:
            for index, existing_item in self._items.items():
                if existing_item == item:
                    self.view.takeItem(index)
                    del self._items[index]
                    del self._views[index]
                    break

    def remove_selected_row(self):
        """Remove the currently selected row from the listbox."""
        if self.row_is_selected:
            index = self.selected_index
            self.view.takeItem(index)
            del self._items[index]
            del self._views[index]

    def clear(self):
        """Remove all rows from the listbox."""
        self.view.clear()
        self._items.clear()
        self._views.clear()

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item click event."""
        index = self.view.row(item)
        self.itemClicked.emit(self._items[index], self._views[index])