from codiet.utils import SingletonMeta

class OptimiserFixtures(metaclass=SingletonMeta):

    def __init__(self):
        self._monday_structure = {
            "Breakfast": {
                "Drink": {},
                "Main": {}
            },
            "Lunch": {
                "Main": {},
                "Side": {}
            },
            "Dinner": {
                "Main": {},
                "Side": {}
            }
        }

    @property
    def monday_structure(self):
        return self._monday_structure