import json
import os

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "C:\\Users\\james\\Dropbox\\CoDiet\\codiet\\db\\ingredient_data")

# Open each ingredient json file and load its json contents
# Get a list of all json files in the current directory
json_files = [f for f in os.listdir(INGREDIENT_DATA_DIR) if f.endswith('.json')]
# For each file, load the data
for json_file in json_files:
    with open(os.path.join(INGREDIENT_DATA_DIR, json_file), 'r') as f:
        print(f"Loading {json_file}...")
        data = json.load(f)
        # Create a new nutrients dict
        new_nutrients = {}
        # For each nutrient in the json contents
        for nutrient in data['nutrients'].keys():
            # Move the data into the new dict
            new_nutrients[nutrient] = {}
            new_nutrients[nutrient]['ntr_qty_value'] = data['nutrients'][nutrient]["quantity"]["value"]
            new_nutrients[nutrient]['ntr_qty_unit'] = data['nutrients'][nutrient]["quantity"]["unit"]
            new_nutrients[nutrient]['ing_qty_value'] = data['nutrients'][nutrient]["in_serving_size"]["value"]
            new_nutrients[nutrient]['ing_qty_unit'] = data['nutrients'][nutrient]["in_serving_size"]["unit"]
        # Replace the old nutrients dict with the new one
        data['nutrients'] = new_nutrients
    # Save the ingredient file back to the fs
    with open(os.path.join(INGREDIENT_DATA_DIR, json_file), 'w') as f:
        print(f"Saving {json_file}...")
        json.dump(data, f)