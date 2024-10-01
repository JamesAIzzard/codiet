from .goal import Goal

class MinimiseNutrientGoal(Goal):
    
    def __init__(self, nutrient_name:str):
        self.nutrient_name = nutrient_name