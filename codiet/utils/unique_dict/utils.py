
def check_values_are_unique(items):
    if len(set(items.values())) != len(items.values()):
        raise ValueError("Values must be unique")