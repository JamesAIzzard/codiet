# from typing import Collection
# from unittest import skip

# from codiet.tests import BaseCodietTest
# from codiet.tests.fixtures import ConstraintTestFixtures, RecipeTestFixtures, OptimiserTestFixtures
# from codiet.optimisation.optimiser import Optimiser
# from codiet.optimisation.constraints import FlagConstraint, TagConstraint
# from codiet.optimisation.problems import Problem
# from codiet.optimisation.solutions import Solution

# class BaseOptimiserTest(BaseCodietTest):
#     def setUp(self) -> None:
#         super().setUp()
#         self.constraint_fixtures = ConstraintTestFixtures.get_instance()
#         self.recipe_fixtures = RecipeTestFixtures.get_instance()
#         self.optimiser_fixtures = OptimiserTestFixtures.get_instance()

# class TestConstructor(BaseOptimiserTest):
    
#     def test_can_create_optimiser(self):
#         optimiser = Optimiser()

#         self.assertIsInstance(optimiser, Optimiser)

# class TestSolve(BaseOptimiserTest):
    
#     def test_returns_collection_of_solutions(self):
#         optimiser = self.optimiser_fixtures.deterministic_optimiser

#         # We can create a problem like this...
#         problem1 = DietProblem(
#             {
#                 "Breakfast": {
#                     "Drink": {},
#                     "Main": {}
#                 }
#             }
#         )

#         # Or like this...
#         problem2 = DietProblem()
#         problem2.add_subproblem("Breakfast")
#         problem2["Breakfast"].add_subproblem("Drink")
#         problem2["Breakfast"].add_subproblem("Main")

#         # Or a hybrid of the two...
#         problem1.add_subproblem("Lunch", {
#             "Main": {},
#             "Side": {}
#         })

#         # We can add constraints to any level of the tree like this...
#         problem1["Breakfast"].add_constraint(FlagConstraint('vegan', True))
#         problem1["Breakfast"]["Drink"].add_constraint(TagConstraint("drink"))
#         problem1["Breakfast"]["Main"].add_constraint(TagConstraint("cereal"))

#         # Then we run the optimiser and it gives us a collection of solutions...
#         results = optimiser.solve(problem1)

#         # Inside each result, there is now a Recipe instance at each leaf node of the tree...
#         for solution in results:
#             self.assertIsInstance(solution, DietSolution)
#             self.assertIsInstance(solution["Breakfast"], Recipe)
#             self.assertIsInstance(solution["Breakfast"]["Drink"], Recipe)
#             self.assertIsInstance(solution["Breakfast"]["Main"], Recipe)

#         # The solution structure is immutable...
#         solution = results[0]
#         with self.assertRaises(AttributeError):
#             results["Breakfast"] = Recipe()

    
#     def test_all_diet_plans_satisfy_recipe_problem_flag_constraints(self):
#         optimiser = self.optimiser_fixtures.deterministic_optimiser

#         problem = Problem({"Breakfast": {}})
#         problem["Breakfast"].add_constraint(FlagConstraint("vegan", True))
#         problem["Breakfast"].add_constraint(FlagConstraint("gluten_free", True))

#         results = optimiser.solve(problem)

#         for solution in results:
#             self.assertTrue(solution["Breakfast"].get_flag("vegan").value)
#             self.assertTrue(solution["Breakfast"].get_flag("gluten_free").value)