import os
import json
import hashlib

from decouple import config
from pathlib import Path
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError


def generate_unique_id(header, fecha):
    # Generate a unique identifier based on header and fecha.
    unique_string = f"{header}{fecha}"
    return hashlib.md5(unique_string.encode("utf-8")).hexdigest()


class MongoDBHandler:
    def __init__(self, uri, database_name, collection_name):
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi("1"))
            db = self.client[self.database_name]
            self.collection = db[self.collection_name]
            print(f"Successfully connected to MongoDB database: {self.database_name}")
        except PyMongoError as e:
            print(f"MongoDB connection error: {e}")
            raise

    def insert_data(self, data):
        try:
            # Validate the type of data
            if not isinstance(data, (list, dict)):
                raise ValueError("Data must be a list or a dictionary.")

            # Insert data based on its type
            if isinstance(data, list):
                for item in data:
                    existing = self.collection.find_one(
                        {"header": item["header"], "titulo": item["titulo"]}
                    )
                if not existing:
                    self.collection.insert_one(item)
                    print(f"Inserted: {item['header']}")
                else:
                    print(f"Duplicate found, skipped: {item['header']}")

                result = self.collection.insert_many(data)
                print(f"Inserted {len(result.inserted_ids)} items into the collection.")

            elif isinstance(data, dict):
                existing = self.collection.find_one(
                    {"header": data["header"], "titulo": data["titulo"]}
                )

                if not existing:
                    self.collection.insert_one(data)
                    print(f"Inserted: {data['header']}")
                else:
                    print(f"Duplicate found, skipped: {data['header']}")
            else:
                print("Data format is not supported for insertion.")
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")


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
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                data = json.load(file)
                mongo_handler.insert_data(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


def main():
    # Configuration
    uri = config("MONGO_URI")
    database_name = "La-Justa"
    collection_name = "news"

    # Initialize handlers
    mongo_handler = MongoDBHandler(uri, database_name, collection_name)
    mongo_handler.connect()

    project_root = Path(__file__).resolve().parent.parent  # Go up 2 levels
    results_folder = project_root / "results"

    json_processor = JSONProcessor(results_folder)
    json_processor.process_files(mongo_handler)

    print("All data successfully processed and inserted into MongoDB.")
    
if __name__ == "__main__":
    main()
