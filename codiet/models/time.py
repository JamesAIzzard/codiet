from codiet.utils.time import convert_time_string_interval_to_datetime_interval

class RecipeServeTimeWindow:
    def __init__(self, id: int, recipe_id: int, window_string: str):
        self.id = id
        self.recipe_id = recipe_id
        self.window_string = window_string.replace(" ", "")
        self.datetime_interval = convert_time_string_interval_to_datetime_interval(window_string)