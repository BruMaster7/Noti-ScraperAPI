# Noti-ScraperAPI

Noti-ScraperAPI is a powerful toolchain designed for scraping news from multiple sources, processing them, storing them in a MongoDB database, and serving them via a RESTful API. This project is ideal for developers who need a streamlined system to gather and serve news data efficiently.

---

## Features

### 1. **News Scraper**

- Scrapes news articles from supported websites (using BeautifulSoup).
- Modular design with parsers for specific sources (e.g., El País, Montevideo Portal, Xataka).
- Outputs JSON files containing scraped data.

### 2. **MongoDB Integration**

- Handles data storage in a MongoDB Atlas database.
- Ensures efficient insertion and retrieval of news data.

### 3. **RESTful API**

- Built with **FastAPI** for high performance and easy scalability.
- Provides endpoints for paginated and filtered news retrieval.
- Designed to seamlessly integrate with front-end applications.

---

## Project Structure

```
noti_scraperapi/
├── api/
│   ├── main.py               # Main FastAPI application for the REST API
│   ├── README.md             # Documentation for the REST API
├── data/
│   ├── .gitkeep              # Placeholder to track the folder
│   └── (JSON files)          # Folder for storing scraped JSON data (ignored in .gitignore)
├── mongo_utils/
│   ├── json_processor.py     # Utility for processing JSON files
│   ├── main.py               # Entry point for MongoDB-related scripts
│   ├── mongodb_handler.py    # MongoDB connection and operations handler
├── src/noti_scraperapi/
│   ├── article_parsers/      # Parsers for articles from various sources
│   │   ├── base.py           # Base parser class
│   │   ├── el_pais.py        # Parser for "El País"
│   │   ├── montevideo_portal.py # Parser for "Montevideo Portal"
│   │   ├── xataka.py         # Parser for "Xataka"
│   ├── new.py                # New class
│   ├── scrapers.py           # Main scrapers for fetching articles
│   ├── util.py               # Utility functions
├── .env                      # Environment variables (must be created by the user)
├── .gitignore                # Git ignore rules
├── .python-version           # Specifies Python version
```

---

## 🔧 Technologies & Tools

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge)
![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?logo=mongodb&logoColor=white&style=for-the-badge)
![Rye](https://img.shields.io/badge/-Rye-FAB040?logo=python&logoColor=white&style=for-the-badge)

</div>

---

## Installation

### Prerequisites

- **Python 3.10+**
- **MongoDB Atlas** account
- **Rye** (for Python project management)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/BruMaster7/Noti-ScraperAPI.git
   cd noti-scraperapi
   ```

2. Create and configure your `.env` file:

   ```
   MONGO_URI=<your-mongodb-uri>
   MONGO_DB=<Database Name>
   MONGO_COLLECTION=<Name of the collection>
   ```

3. Install dependencies:

   ```bash
   rye sync
   ```

4. Run the API:

   ```bash
   rye run uvicorn api.main:app --reload
   ```

5. Access the API documentation at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Usage

### Scraping Data

- Use the scripts in `src/noti_scraperapi/scrapers.py` to scrape articles from supported websites.
- Scraped data is stored as JSON files in the `data/` directory.

**Run the scraper in console:**

    rye run xataka/montevideo_portal/el_pais
    

### MongoDB Integration

- Use `src/mongo_utils/mongodb_handler.py` to insert scraped data into MongoDB Atlas.

**Add the JSONS to a MongoDB with:**
   ```bash
   rye run connect_to_mongo
   ```

### API Endpoints

#### Base Endpoint

- `GET /`: Welcome message.

#### News Retrieval

- `GET /news`: Retrieve news with optional pagination and filters.
  - Query Parameters:
    - `page`: Page number (default: 1).
    - `page_size`: Number of results per page (default: 10, max: 100).
    - `title`: Filter by title (case-insensitive).
    - `header`: Filter by header (case-insensitive).
    - `category`: Filter by category (case-insensitive).

#### Example Request:

```bash
curl "http://127.0.0.1:8000/news?page=1&page_size=5&title=Technology"
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

---


