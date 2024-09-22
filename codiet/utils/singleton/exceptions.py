class SingletonInitError(Exception):
    """Exception raised when there is an error initializing a singleton."""
    def __init__(self, message: str = "Error initializing singleton instance"):
        self.message = message
        super().__init__(self.message)