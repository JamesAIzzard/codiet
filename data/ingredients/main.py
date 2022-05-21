import model
import data 

def save_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    qry = f"""INSERT INTO ingredients(
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
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    conn.commit()