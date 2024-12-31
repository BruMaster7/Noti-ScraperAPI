from decouple import config
from pathlib import Path

from mongodb_handler import MongoDBHandler
from json_processor import JSONProcessor


def main():
    # Configuration
    uri = config("MONGO_URI")
    database_name = config("MONGO_DB")
    collection_name = config("MONGO_COLLECTION")

    # Initialize handlers
    mongo_handler = MongoDBHandler(uri, database_name, collection_name)
    mongo_handler.connect()

    # For clear the collection before inserting new data add:
    mongo_handler.clear_collection()

    project_root = Path(__file__).resolve().parent.parent  # Go up 2 levels
    results_folder = project_root / "data"

    json_processor = JSONProcessor(results_folder)
    json_processor.process_files(mongo_handler)

    print("All data successfully processed and inserted into MongoDB.")


if __name__ == "__main__":
    main()
