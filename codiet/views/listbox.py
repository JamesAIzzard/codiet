from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
)

class ListBox(QListWidget):
    """Customised version of the listbox widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def selected_item(self) -> QListWidgetItem|None:
        """Return the selected result."""
        if self.item_is_selected:
            return self.currentItem()
        else:
            return None

    @property
    def selected_index(self) -> int:
        """Return the index of the selected result."""
        return self.currentRow()

    @property
    def item_is_selected(self) -> bool:
        """Return True if a result is selected."""
        return self.selected_index != -1

    def add_item(self, result: QWidget | str) -> None:
        """Add a result to the search column."""
        if isinstance(result, str):
            self.addItem(result)        
        elif isinstance(result, QWidget):          
            item = QListWidgetItem(self)
            item.setSizeHint(result.sizeHint())
            self.setItemWidget(item, result)
        else:
            raise ValueError(f"Unsupported result type: {type(result)}")
        
    def remove_item(self, index: int|None=None, item: QListWidgetItem|None=None) -> None:
        """Remove a result from the search column."""
        if item is not None:
            self.takeItem(self.row(item))
        elif index is not None:
            self.takeItem(index)
        else:
            raise ValueError("You must provide either an index or an item to remove.")
        
    def remove_selected_item(self) -> None:
        """Remove the selected result from the search column."""
        if self.item_is_selected:
            self.remove_item(index=self.selected_index)

    def update_list(self, matching_results: list[QWidget | str]):
        """Update the results list to reflect the matching results."""
        # Clear the existing ingredients
        self.clear()
        # Add the matching ingredients
        for result in matching_results:
            self.add_item(result)

    def clear_list(self):
        """Clear the search results."""
        self.clear()