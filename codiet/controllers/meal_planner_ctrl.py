from codiet.db.database_service import DatabaseService
from codiet.views.meal_planner_view import MealPlannerView

class MealPlannerCtrl:
    """Controller for the Meal Planner page."""
    def __init__(self, view: MealPlannerView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service
        