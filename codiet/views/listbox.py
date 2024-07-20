from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import pyqtSignal

class ListBox(QListWidget):
    """Customised version of the listbox widget.

    Notes:
    The distinction between the view item, the view item content and
    the data associated with the view item is important.
    - View Item: The QListWidgetItem that is displayed in the list box.
    - View Item Content: The content of the view item. This can be a string or a widget.
    - Data: The data associated with the view item. This can be any object.

    Signals:
        itemClicked: Emitted when an item is clicked. The signal is emitted with the item content and data.
    """

    itemClicked = pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Connect the item selection changed signal to the _on_result_selected method
        self.itemClicked.connect(self._on_item_clicked)

    @property
    def selected_item(self) -> QListWidgetItem|None:
        """Return the selected result.
        Returns:
            QListWidgetItem|None: The selected item or None if no item is selected.
        """
        if self.item_is_selected:
            return self.currentItem()
        else:
            return None
        
    @property
    def selected_item_content(self) -> str|QWidget|None:
        """Return the content of the selected result.
        Returns:
            str|QWidget|None: The content of the selected item or None if no item is selected.
        """
        if self.item_is_selected:
            item = self.currentItem()
            if self.itemWidget(item):
                return self.itemWidget(item)
            else:
                return item.text() # type: ignore
        else:
            return None
        
    @property
    def selected_item_data(self) -> Any:
        """Return the data associated with the selected result.
        Returns:
            Any: The data associated with the selected item or None if no item is selected.
        """
        if self.item_is_selected:
            item = self.currentItem()
            return item.data(Qt.ItemDataRole.UserRole) # type: ignore
        else:
            return None
        
    @property
    def all_items_content_and_data(self) -> list[tuple[str|QWidget, Any]]:
        """Return the content and data of all items in the list.
        Returns:
            list[tuple[str|QWidget, Any]]: A list of tuples containing the content and data for each item.
        """
        items = []
        for i in range(self.count()):
            item = self.item(i)
            # If the widget is not None
            if self.itemWidget(item):
                # grab the content from the widget
                content = self.itemWidget(item)
            else:
                # otherwise grab the text content from the item
                content = item.text() # type: ignore
            # Grab the data associated with the item
            data = item.data(Qt.ItemDataRole.UserRole) # type: ignore
            items.append((content, data))
        return items
    
    @property
    def all_items_and_data(self) -> list[tuple[QListWidgetItem, Any]]:
        """Return all items and their associated data.
        Returns:
            list[tuple[QListWidgetItem, Any]]: A list of tuples containing the item and data for each item.
        """
        items = []
        for i in range(self.count()):
            item = self.item(i)
            data = item.data(Qt.ItemDataRole.UserRole) # type: ignore
            items.append((item, data))
        return items

    @property
    def selected_index(self) -> int:
        """Return the index of the selected result.
        Returns:
            int: The index of the selected item or -1 if no item is selected.
        """
        return self.currentRow()

    @property
    def item_is_selected(self) -> bool:
        """Return True if a result is selected.
        Returns:
            bool: True if a result is selected, False otherwise."""
        return self.selected_index != -1

    def add_item(self, item: QListWidgetItem, data: Any = None) -> None:
        """Add a QListWidgetItem to the list box.

        Args:
            item (QListWidgetItem): The item to add.
            data (Any, optional): The data to associate with the item. Defaults to None.
        """
        if data is not None:
            item.setData(Qt.ItemDataRole.UserRole, data)
        self.addItem(item)

    def add_item_content(self, item_content: str | QWidget, data: Any = None) -> QListWidgetItem:
        """Add an item to the list box.
        The item content can be a string or a widget. The string or widget are passed in as the 
        item_content argument. The method converts the item_content to a QListWidgetItem and
        adds it to the list box. The data argument is optional and can be used to associate
        data with the item, for example a model's UID from the database.
        Args:
            item_content (str | QWidget): The content of the item.
            data (Any, optional): The data to associate with the item. Defaults to None.
        Returns:
            QListWidgetItem: The item that was added.
        """
        if isinstance(item_content, str):
            item = QListWidgetItem(item_content)
            self.addItem(item)
        elif isinstance(item_content, QWidget):
            item = QListWidgetItem(self)
            item.setSizeHint(item_content.sizeHint())
            self.setItemWidget(item, item_content)
        else:
            raise ValueError(f"Unsupported content type: {type(item_content)}")
        
        if data is not None:
            item.setData(Qt.ItemDataRole.UserRole, data)
        
        return item
        
    def remove_item(self, index: int|None=None, item: QListWidgetItem|None=None, data: Any|None=None) -> None:
        """Remove a result from the search column.
        Args:
            index (int, optional): The index of the item to remove. Defaults to None.
            item (QListWidgetItem, optional): The item to remove. Defaults to None.
            data (Any, optional): The data associated with the item. Defaults to None.
        Returns:
            None
        """
        if item is not None:
            self.takeItem(self.row(item))
        elif index is not None:
            self.takeItem(index)
        elif data is not None:
            for i in range(self.count()):
                item = self.item(i)
                if item and item.data(Qt.ItemDataRole.UserRole) == data:
                    self.takeItem(i)
                    break
        else:
            raise ValueError("You must provide either an index or an item to remove.")
        
    def remove_selected_item(self) -> None:
        """Remove the selected result from the search column."""
        if self.item_is_selected:
            self.remove_item(index=self.selected_index)

    def data_in_list(self, data: Any) -> bool:
        """Check if the data is in the list.
        Args:
            data (Any): The data to check for.
        Returns:
            bool: True if the data is in the list, False otherwise.
        """
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == data:
                return True
        return False

    def get_item_for_data(self, data: Any) -> QListWidgetItem:
        """Return the view item associated with the data.
        Args:
            data (Any): The data associated with the item.
        Returns:
            QListWidgetItem: The view item associated with the data.
        Raises:
            ValueError: If no item is found for the data.
        """
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == data:
                return item
        raise ValueError(f"No item found for data: {data}")

    def get_data_for_item(self, item: QListWidgetItem) -> Any:
        """Return the data associated with the item.
        Args:
            item (QListWidgetItem): The item to get the data for.
        Returns:
            Any: The data associated with the item.
        Raises:
            ValueError: If no data is found for the item.
        """
        data = item.data(Qt.ItemDataRole.UserRole)
        if data is None:
            raise ValueError(f"No data found for item: {item}")
        return data

    def get_widget_for_data(self, data: Any) -> str | QWidget:
        """Return the view item associated with the data.
        Args:
            data (Any): The data associated with the item.
        Returns:
            str | QWidget: The view item (either a string or a widget) associated with the data.
        Raises:
            ValueError: If no item is found for the data.
        """
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == data:
                return self.itemWidget(item) or item.text()
        raise ValueError(f"No item found for data: {data}")

    def update_list(self, item_content_and_data: list[tuple[QWidget | str, Any]]) -> None:
        """Update the list to the item content and associated data. Clears any existing items.
        Args:
            content_and_data (list[tuple[QWidget | str, Any]]): A list of tuples containing the content and data for each result.
        Returns:
            None
        """
        self.clear()
        for item_content, data in item_content_and_data:
            self.add_item_content(item_content=item_content, data=data)

    def _on_item_clicked(self):
        """Called when a result is selected.
        Emits the item content and its associated data.
        """
        if self.item_is_selected:
            item = self.currentItem()
            assert item is not None
            data = item.data(Qt.ItemDataRole.UserRole)
            
            # Get the content based on whether it's a string or a widget
            if self.itemWidget(item):
                content = self.itemWidget(item)
            else:
                content = item.text()
            
            self.itemClicked.emit(content, data)