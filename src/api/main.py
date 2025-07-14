from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from decouple import config
from threading import Thread

from api.cron_tasks import run_scheduler, schedule_tasks
from mongo_utils.mongodb_handler import MongoDBHandler

app = FastAPI()

origins = [
    "https://la-justa-noticias.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uri = config("MONGO_URI")
database_name = config("MONGO_DB")
collection_name = config("MONGO_COLLECTION")

# Connect to Mongo
mongo_handler = MongoDBHandler(uri, database_name, collection_name)
mongo_handler.connect()

def start_cron():
    schedule_tasks()
    run_scheduler()

@app.on_event("startup")
def startup_event():
    cron_thread = Thread(target=start_cron, daemon=True)
    cron_thread.start()
    print("Cron running in the background")

@app.on_event("shutdown")
async def shutdown_event():
    print("Closing the application, cron finished")

@app.get("/")
async def root():
    return {"message": "Welcome to Noti-Scraper API! Use /news to fetch news data."}


@app.get("/news")
async def get_news(
    page: int = Query(1, ge=1),  # Page number (default 1, must be >= 1)
    page_size: int = Query(
        10, ge=1, le=100
    ),  # Page size (default 10, between 1 and 100)
    title: Optional[str] = None,  # Filter by title (optional)
    header: Optional[str] = None,  # Filter by header (optional)
    category: Optional[str] = None,  # Filter by category (optional)
    sort_order: str = Query("desc", regex="^(asc|desc)$"),  # Sorting order: asc/desc
):
    try:
        filters = {}
        if title:
            filters["title"] = {
                "$regex": title,
                "$options": "i",
            }  # Case-insensitive search
        if header:
            filters["header"] = {
                "$regex": header,
                "$options": "i",
            }  # Case-insensitive search
        if category:
            filters["category"] = {
                "$regex": category,
                "$options": "i",
            }  # Case-insensitive search

        # Pagination calculations
        skip = (page - 1) * page_size
        limit = page_size

         # Sorting order based on sort_order parameter
        sort_direction = -1 if sort_order == "desc" else 1

        
        # Fetch data with filters and pagination
        news_cursor = (
            mongo_handler.collection
            .find(filters, {"_id": 0})
            .sort("date", sort_direction)
            .skip(skip)
            .limit(limit)
        )
        news = list(news_cursor)

        # Count the total number of documents matching the filter
        total_count = mongo_handler.collection.count_documents(filters)

        return {
            "data": news,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": (total_count + page_size - 1)
                // page_size,  # Total number of pages
            },
        }
    except Exception as e:
        return {"error": str(e)}
