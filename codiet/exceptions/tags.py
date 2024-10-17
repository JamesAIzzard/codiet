class TagNotFoundError(ValueError):
    def __init__(self, tag_name: str):
        self.tag = tag_name
        self.message = f"Tag {tag_name} is not defined in the database."

    def __str__(self):
        return self.message