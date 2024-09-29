import os

def get_data_dir_path(object_name: str) -> str:
    current_dir = os.path.dirname(__file__)
    if object_name == "units":
        return os.path.join(current_dir, "quantities", "quantities_data")
    elif object_name == "global_unit_conversions":
        return os.path.join(current_dir, "quantities", "quantities_data")
    else:
        raise ValueError(f"Unknown object name {object_name}")