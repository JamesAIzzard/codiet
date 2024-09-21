class SingletonMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls._instance = None

    def initialise(cls, *args, **kwargs):
        if cls._instance is None:
            # First-time initialization
            cls._instance = super().__call__(*args, **kwargs)
        else:
            # Re-initialize the existing instance
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def get_instance(cls):
        if cls._instance is None:
            raise Exception("Singleton instance not initialized. Call 'initialize' first.")
        return cls._instance

