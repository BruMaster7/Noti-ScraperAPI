import os
import json

from pathlib import Path


class JSONProcessor:
    # Handles processing of JSON files.

    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)

    def process_files(self, mongo_handler):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                file_path = self.folder_path / filename
                self._process_file(file_path, mongo_handler)

    def _process_file(self, file_path, mongo_handler):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                data = json.load(file)
                mongo_handler.insert_data(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
