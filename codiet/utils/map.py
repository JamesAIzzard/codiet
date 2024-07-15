class IntStrMap:
    """A bidirectional map that stores a mapping between integers and strings."""
    def __init__(self):
        self.int_to_str = {}
        self.str_to_int = {}

    @property
    def int_values(self) -> list[int]:
        """Return a list of integer keys."""
        return list(self.int_to_str.keys())
    
    @property
    def str_values(self) -> list[str]:
        """Return a list of string keys."""
        return list(self.str_to_int.keys())

    def add_mapping(self, integer:int, string:str) -> None:
        """Add a new mapping between an integer and a string."""
        if integer in self.int_to_str:
            raise ValueError("Integer key already exists in the map.")
        if string in self.str_to_int:
            raise ValueError("String value already exists in the map.")
        
        self.int_to_str[integer] = string
        self.str_to_int[string] = integer

    def remove_mapping_by_int(self, integer) -> None:
        """Remove a mapping by its integer key."""
        if integer in self.int_to_str:
            string = self.int_to_str.pop(integer)
            del self.str_to_int[string]
        else:
            raise KeyError("Integer key not found in the map.")

    def remove_mapping_by_str(self, string) -> None:
        """Remove a mapping by its string key."""
        if string in self.str_to_int:
            integer = self.str_to_int.pop(string)
            del self.int_to_str[integer]
        else:
            raise KeyError("String value not found in the map.")

    def get_str(self, integer) -> str:
        """Return the string value for a given integer key, or None if not found."""
        return self.int_to_str.get(integer, None)

    def get_int(self, string) -> int:
        """Return the integer key for a given string value, or None if not found."""
        return self.str_to_int.get(string, None)
