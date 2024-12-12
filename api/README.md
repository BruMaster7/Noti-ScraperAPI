# Noti-Scraper API

Noti-Scraper API is a RESTful API built with FastAPI for fetching news data stored in MongoDB. This project leverages the Rye package manager for Python for dependency management and running the application.

## Features
- Fetch paginated news data
- Filter news by title, header, or category
- Lightweight and efficient

---

## Requirements

Before you begin, ensure you have the following installed:

- Python 3.10+
- [Rye](https://rye-up.com/) (Python toolchain manager)
- MongoDB Atlas or a local MongoDB instance

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BruMaster7/Noti-ScraperAPI
   cd Noti-ScraperAPI
   ```

2. **Install Dependencies with Rye:**
   Rye automatically detects the dependencies specified in the `pyproject.toml` file.
   ```bash
   rye sync
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```env
   MONGO_URI=your_mongodb_uri
   MONGO_DB=your_database_name
   MONGO_COLLECTION=your_collection_name
   ```
   Replace `your_mongodb_uri`, `your_database_name`, and `your_collection_name` with your MongoDB configuration.

4. **Run the Application:**
   Use Rye to start the application.
   ```bash
   rye run uvicorn api.main:app --reload
   ```

   The application will be available at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### `GET /`
Returns a welcome message.

**Response:**
```json
{
    "message": "Welcome to Noti-Scraper API! Use /news to fetch news data."
}
```

### `GET /news`
Fetches news with optional pagination and filters.

#### Query Parameters:
- `page` (int): Page number (default: 1, must be ≥1)
- `page_size` (int): Number of items per page (default: 10, max: 100)
- `title` (str, optional): Filter by title (case-insensitive)
- `header` (str, optional): Filter by header (case-insensitive)
- `category` (str, optional): Filter by category (case-insensitive)

#### Example Request:
```bash
curl "http://127.0.0.1:8000/news?page=1&page_size=5&title=technology"
```

#### Example Response:
```json
{
    "data": [
        {
            "title": "Technology News",
            "header": "Latest Innovations",
            "category": "Technology"
        }
    ],
    "pagination": {
        "current_page": 1,
        "page_size": 5,
        "total_items": 50,
        "total_pages": 10
    }
}
```

---

## Project Structure
```
noti_scraperapi/
├── api/
│   ├── main.py               # Main FastAPI application for the REST API
│   ├── README.md             # Documentation for the API
├── data/
│   ├── .gitkeep              # Placeholder to ensure the folder exists in version control
│   └── (JSON files)          # Folder for storing scraped JSON data (ignored in .gitignore)
├── mongo_utils/
│   ├── json_processor.py     # Utility for processing JSON files
│   ├── main.py               # Entry point for other MongoDB-related scripts
│   ├── mongodb_handler.py    # MongoDB connection and operations handler
├── src/noti_scraperapi/
│   ├── article_parsers/      # Module for parsing articles from different sources
│   │   ├── __init__.py       # Module initializer
│   │   ├── base.py           # Base parser class with shared functionality
│   │   ├── el_pais.py        # Parser for articles from "El País"
│   │   ├── montevideo_portal.py # Parser for "Montevideo Portal"
│   │   ├── xataka.py         # Parser for "Xataka"
│   ├── new.py                # New class
│   ├── scrapers.py           # Main scrapers for fetching articles
│   ├── util.py               # Utility functions used across the project
├── .env                      # Environment variables (must be created by the user)
├── .python-version           # Specifies Python version used for the project

```

---

## Development Notes

- **Why Rye?**
  Rye simplifies dependency management and project setup by handling virtual environments and dependencies automatically.

- **Running Tests:**
  Add your test suite and run tests using Rye (e.g., `rye run pytest`).

---

## Future Improvements

- Add more endpoints (e.g., POST, PUT, DELETE)
- Integrate additional filters
- Enhance error handling

---



