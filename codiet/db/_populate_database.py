import os, json

from codiet.db.database_service import DatabaseService

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")


def _populate_flags(db_service: DatabaseService):
    # Define list of flags
    flags = [
        "alcohol free",
        "caffeine free",
        "gluten free",
        "lactose free",
        "nut free",
        "vegan",
        "vegetarian",
    ]
    # Add each flag to the database
    for flag in flags:
        db_service.repo.add_flag(flag)


def _populate_ingredients(db_service: DatabaseService):
    # Work through each .json file in the ingredient_data directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Add the ingredient name to the database, getting primary key
        db_service.repo.add_ingredient_name(data["name"])

        # Get the ingredient ID from the database
        ingredient_id = db_service.repo.get_ingredient_id(data["name"])

        # Add the ingredient cost data
        db_service.repo.set_ingredient_cost(
            ingredient_id=ingredient_id,
            cost_unit=data["cost"]["cost_unit"],
            cost_value=data["cost"]["cost_value"],
            mass_unit=data["cost"]["qty_unit"],
            mass_value=data["cost"]["qty_value"],
        )

        # Add the ingredient density data
        db_service.repo.set_ingredient_density(
            ingredient_id=ingredient_id,
            dens_mass_unit=data["bulk"]["density"]["mass_unit"],
            dens_mass_value=data["bulk"]["density"]["mass_value"],
            dens_vol_unit=data["bulk"]["density"]["vol_unit"],
            dens_vol_value=data["bulk"]["density"]["vol_value"],
        )
