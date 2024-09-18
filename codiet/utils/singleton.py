class SingletonMeta(type):
    """A metaclass that creates a Singleton base type when called."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create and initialize a new instance if it doesn't exist
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        # Return the existing instance without re-initializing
        return cls._instances[cls]

    def get_instance(cls):
        """Returns the singleton instance of the class."""
        if cls not in cls._instances:
            raise Exception(f"{cls.__name__} has not been initialized yet.")
        return cls._instances[cls]

    def reset_instance(cls):
        """Resets the singleton instance of the class."""
        if cls in cls._instances:
            del cls._instances[cls]

    @classmethod
    def reset_all_instances(mcs):
        """Resets all singleton instances."""
        mcs._instances.clear()
