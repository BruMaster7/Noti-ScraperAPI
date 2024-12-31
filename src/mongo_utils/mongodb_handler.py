from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError


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

    def clear_collection(self):
        # Delete all documents from the collection.
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from the collection.")

    def insert_data(self, data):
        try:
            if not isinstance(data, (list, dict)):
                raise ValueError("Data must be a list or a dictionary.")

            if isinstance(data, list):
                for item in data:
                    if "date" in item:
                        item["date"] = self._convert_to_date(item["date"])
                    existing = self.collection.find_one(
                        {"header": item["header"], "title": item["title"]}
                    )
                    if not existing:
                        self.collection.insert_one(item)
                        print(f"Inserted: {item['header']}")
                    else:
                        print(f"Duplicate found, skipped: {item['header']}")

            elif isinstance(data, dict):
                if "date" in data:
                    data["date"] = self._convert_to_date(data["date"])
                existing = self.collection.find_one(
                    {"header": data["header"], "title": data["title"]}
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
            
    def _convert_to_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except ValueError as e:
            print(f"Error converting date: {date_str}, {e}")
            return None 
