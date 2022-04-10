from typing import List

class User:
    def __init__(self):
        self.global_flags: List[str] = []

    def add_global_flag(self, flag:str) -> None:
        """Adds a flag to the user's list of global flags."""
        if flag not in self.global_flags:
            self.global_flags.append(flag)

# Create the global user instance
user: User = User()