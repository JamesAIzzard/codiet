from typing import Collection
from unittest import skip

from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.constraints import ConstraintTestFixtures
from codiet.tests.fixtures.recipes import RecipeTestFixtures
from codiet.optimisation.optimiser import Optimiser
from codiet.optimisation import algorithms
from codiet.model.diet_plan import DietPlan

class BaseOptimiserTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()
        self.constraint_fixtures = ConstraintTestFixtures.get_instance()
        self.recipe_fixtures = RecipeTestFixtures.get_instance()

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_returns_collection_of_diet_plans(self):
        constraints = [
            self.constraint_fixtures.create_flag_constraint('vegan', True),
            self.constraint_fixtures.create_flag_constraint('gluten_free', True),
        ]

        optimiser = Optimiser()
        optimiser.set_recipe_source(self.recipe_fixtures.recipes.values())
        optimiser.set_constraints(constraints)
        optimiser.set_algorithm(algorithms.Deterministic())

        results = optimiser.solve()

        self.assertIsInstance(results, Collection)
        for item in results:
            self.assertIsInstance(item, DietPlan)

    @skip("In progress")
    def test_all_diet_plans_satisfy_flag_constraints(self):

        day1 = DayProblem("Day 1")
        day1_breakfast = MealProblem("Breakfast")
        day1_breakfast_drink = RecipeProblem("Drink")
        day1_breakfast_main = RecipeProblem("Main")
        day1_breakfast.add_recipe_problem(day1_breakfast_drink)
        day1_breakfast.add_recipe_problem(day1_breakfast_main)
        day1_breakfast_drink.add_constraint(TagConstraint("drink"))
        day1_breakfast_main.add_constraint(TagConstraint("main"))
        day1_breakfast.add_constraint(FlagConstraint("vegan", True))
        day1_breakfast.add_constraint(FlagConstraint("gluten_free", True))
        # day1_breakfast.add_constraint(TimeConstraint("08:00"))
        # day1_breakfast.add_goal(NutrientMassTargetGoal("protein", Quantity(40, "g")))
        # day1_breakfast.add_goal(NutrientMassMinimiseGoal("carbohydrate")
        # day1_breakfast.add_goal(NutrientMassMinimiseGoal("fat"))
        # day1_breakfast.add_goal(CostMinimiseGoal())
        # day1_breakfast.add_goal(CalorieTargetGoal(Quantity(500)))
        day1.add_meal_problem(day1_breakfast)

        optimiser = Optimiser()
        optimiser.set_recipe_source(self.recipe_fixtures.recipes.values())
        optimiser.set_algorithm(algorithms.Deterministic())
        optimiser.set_problem([day1])

        results = optimiser.solve()

        for diet_plan in results:
            self.assertTrue(diet_plan.get_flag('vegan').value)
            self.assertTrue(diet_plan.get_flag('gluten_free').value)