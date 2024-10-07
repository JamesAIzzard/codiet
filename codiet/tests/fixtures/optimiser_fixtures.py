class OptimiserFixtures:

    @property
    def monday_structure(self):
        return {"Monday": {
                "Breakfast": {"Drink": {}, "Main": {}},
                "Lunch": {"Main": {}, "Side": {}},
                "Dinner": {"Main": {}, "Side": {}}
            },
        }