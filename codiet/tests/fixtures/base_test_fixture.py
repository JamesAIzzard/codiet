class BaseTestFixture:
    def __init__(self):
        # Private constructor
        if not hasattr(self, '_initialized'):
            raise RuntimeError("Use FixtureManager to get an instance of this class")
        self._initialized = True

    @classmethod
    def _create_instance(cls):
        instance = cls.__new__(cls)
        instance._initialized = False
        instance.__init__()
        return instance