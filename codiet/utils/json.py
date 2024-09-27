import json

def read_json_data(file_path:str) -> dict:
    with open(file_path, "r") as file:
        return json.load(file)