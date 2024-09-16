class StoredEntity:
    def __init__(self, id: int | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = id

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, value: int | None):
        if value is not None and not isinstance(value, int):
            raise ValueError("ID must be an integer or None")
        self._id = value

    @property
    def is_persisted(self) -> bool:
        return self._id is not None