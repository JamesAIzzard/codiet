import sqlite3

from codiet import model, data

def save_new_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    conn = None
    try:
        # Grab the connection and cursor
        conn, cursor = data.connect()

        # First, save the ingredient to the ingredient table
        cursor.execute(f'''
        INSERT INTO ingredients (
            name, 
            cost_per_ref_qty, 
            cost_ref_qty, 
            cost_pref_unit,
            dens_vol_ref_qty,
            dens_vol_unit,
            dens_mass_ref_qty,
            dens_mass_unit,
            piece_mass_ref_num,
            piece_mass_ref_mass,
            piece_mass_ref_units,
            gi
        ) VALUES (
            '{ingredient.name}',
            '{ingredient.cost_per_ref_qty}',
            '{ingredient.cost_ref_qty}',
            '{ingredient.cost_pref_unit}',
            '{ingredient.dens_vol_ref_qty}',
            '{ingredient.dens_vol_unit}',
            '{ingredient.dens_mass_ref_qty}',
            '{ingredient.dens_mass_unit}',
            '{ingredient.piece_mass_ref_num}',
            '{ingredient.piece_mass_ref_mass}',
            '{ingredient.piece_mass_ref_units}',
            '{ingredient.gi}'
        );
        ''')

        # Now write the positive flags to the ingredient_flag table
        # Grab the ingredient id from the cursor
        ingredient_id = cursor.lastrowid
        for flag in ingredient.flags:
            cursor.execute(f'''
            INSERT INTO ingredient_flags (
                flag_name, ingredient_id
            ) VALUES (
                '{flag}', '{ingredient_id}'
            );
            ''')

        # Now write the nutrient relations to the ingredient_nutrient table
        for nutrient_name, nr_data in ingredient.nutrients.items():
            cursor.execute(f'''
            INSERT INTO ingredient_nutrients (
                ingredient_id, 
                nutrient_name, 
                ingredient_qty, 
                ingredient_qty_unit,
                nutrient_mass,
                nutrient_mass_unit
            ) VALUES (
                '{ingredient_id}',
                '{nutrient_name}',
                '{nr_data["ingredient_qty"]}',
                '{nr_data["ingredient_qty_unit"]}',
                '{nr_data["nutrient_mass"]}',
                '{nr_data["nutrient_mass_unit"]}'
            );
            ''')
            
        # All OK, Commit
        conn.commit()
    except sqlite3.Error as e:
        if conn is not None:
            conn.rollback()
            print(e)
    