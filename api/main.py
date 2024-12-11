from fastapi import FastAPI
from pymongo.collection import Collection
from decouple import config

from mongo_utils.mongodb_handler import MongoDBHandler

app = FastAPI()

uri = config("MONGO_URI")
database_name = config("MONGO_DB")
collection_name = config("MONGO_COLLECTION")

#Connect to Mongo
mongo_handler = MongoDBHandler(uri, database_name, collection_name)
mongo_handler.connect()

@app.get("/")
async def root():
    return {"message": "Welcome to Noti-Scraper API! Use /news to fetch news data."}

@app.get("/news")
async def get_news():
    try:
        news = list(mongo_handler.collection.find({}, {"_id": 0}))  # Whitout ObjectId
        return {"data": news}
    except Exception as e:
        return {"error": str(e)}
