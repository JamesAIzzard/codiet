import enum


class FlagImpliesNutrient(enum.Enum):
    """Enumeration to describe the implication of a flag on a nutrient mass."""

    zero = enum.auto
    non_zero = enum.auto
