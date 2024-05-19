from codiet.views.meal_planner_view import MealPlannerView

class MealPlannerCtrl:
    """Controller for the Meal Planner page."""
    def __init__(self, view: MealPlannerView):
        self.view = view
        