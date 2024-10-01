from typing import Protocol

class DataSource(Protocol):
    def read_unit(self, unit_name: str) -> str:...

# class SingletonMeta(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

class JSONDataSource(DataSource):
    def read_unit(self, unit_name: str) -> str:
        return "unit"

class DataService(DataSource):
    def __init__(self, data_source: DataSource) -> None:
        self._data_source = data_source

    def __getattr__(self, name):
        return getattr(self._data_source, name)

data_service = DataService(JSONDataSource())

print("Done")