from codiet.db.database_service import DatabaseService

from codiet.db_population.units import read_units_from_json
# from codiet.db_population.flags import read_global_flags_from_json
# from codiet.db_population.nutrients import read_global_nutrients_from_json
# from codiet.db_population.ingredients import read_ingredients_from_json
# from codiet.db_population.recipes import read_recipes_from_json

def populate_db_from_json(db_service:DatabaseService) -> None:
    """Uses the data from the .json file modules to populate the database."""
    print("Pushing units to the database...")
    global_units = read_units_from_json()
    db_service.create_global_units(global_units)
    # # Push flags to database
    # global_flags = read_global_flags_from_json()
    # db_service.create_global_flags(global_flags)
    # # Push nutrients to database
    # global_nutrients = read_global_nutrients_from_json()
    # db_service.create_global_nutrients(global_nutrients)
    # # Push ingredients to database
    # ingredients = read_ingredients_from_json()
    # db_service.create_ingredients(ingredients)
    # # Push recipes to database
    # recipes = read_recipes_from_json
    # db_service.create_recipes(recipes)
    # Commit the changes
    db_service.repository.commit()
