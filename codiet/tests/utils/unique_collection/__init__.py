
class Simple:
    def __init__(self, id, some_value):
        self.id = id
        self.some_value = some_value

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)