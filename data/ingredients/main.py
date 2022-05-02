import model
import data 

def save_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    qry = f"""INSERT INTO ingredients
        (name, )
        VALUES
        ('{ingredient.name}');
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    conn.commit()