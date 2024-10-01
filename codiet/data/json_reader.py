from typing import Any
import json
import os

class JSONReader:
    
    def read_file(self, filepath: str) -> dict[str, Any]:
        file_path = os.path.join(filepath)
        with open(file_path, 'r') as file:
            return json.load(file)