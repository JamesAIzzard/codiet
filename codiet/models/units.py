class CustomUnit():
    """A custom measurement unit."""
    def __init__(self, unit_name: str, unit_to_grams_ratio: float):
        self.unit_name = unit_name
        self.unit_to_grams_ratio = unit_to_grams_ratio

    def custom_to_grams(self, custom_value: float) -> float:
        """Converts a custom value to grams."""
        return custom_value * self.unit_to_grams_ratio
    
    def grams_to_custom(self, grams: float) -> float:
        """Converts grams to a custom value."""
        return grams / self.unit_to_grams_ratio