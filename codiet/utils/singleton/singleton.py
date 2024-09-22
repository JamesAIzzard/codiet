from typing import TypeVar, Type, Any

from .exceptions import SingletonInitError

T = TypeVar('T')

class SingletonMeta(type):
    _instance: Any = None

    @classmethod
    def clear_instance(cls):
        cls._instance = None

    def __init__(cls: Type[T], name: str, bases: tuple, namespace: dict):
        super().__init__(name, bases, namespace)

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> None:
        raise Exception(f"Direct instantiation of '{cls.__name__}' is not allowed. Use 'initialise' instead.")

    def initialise(cls: Type[T], *args: Any, **kwargs: Any) -> None:
        if cls._instance is None: # type: ignore
            # First-time initialization
            cls._instance = super().__call__(*args, **kwargs) # type: ignore
        else:
            # Re-initialize the existing instance
            cls._instance.__init__(*args, **kwargs) # type: ignore

    def get_instance(cls: Type[T]) -> T:
        if cls._instance is None: # type: ignore
            raise SingletonInitError(f"Singleton instance of '{cls.__name__}' not initialized. Call 'initialize' first.")
        return cls._instance # type: ignore