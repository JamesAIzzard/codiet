class SingletonMeta(type):
    """A metaclass that creates a Singleton base type when called."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create a new instance if it doesn't exist
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        else:
            # Re-initialize the existing instance
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
    
    def get_instance(cls):
        """Returns the singleton instance of the class."""
        if cls not in cls._instances:
            raise Exception(f"{cls.__name__} has not been initialized yet.")
        return cls._instances[cls]    