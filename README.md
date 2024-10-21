# Amazon Watch Scrapper, FastAPI and LLM Conversational Agent

This pipeline provides the Selenium based data scraping script for Scrapping Amazon product (watches) information, saving them to PostgreSQL database, quering the database using API endpoint with the support of pagination and using this scrapped data to get insight with the help of a LLM-based conversational Agent. 

# Features
* **Web Scraping**: Scrapes watch details (e.g., name, brand, price, rating, etc.) from Amazon using Selenium.
Database Storage: Stores the scraped data in a PostgreSQL database.
* **API Endpoints**: Provides FastAPI-based endpoints to query product data with pagination and filtering options.
* **LLM Integration**: Uses a conversational AI agent to extract insights from the product data.
* **Docker Support**: Full Docker support to run the application, database, and services easily.

# Project Architecture
1. Scraper: A Selenium-based scraper that collects product details such as:
    * Product Name
    * Brand
    * Model
    * Price
    * Rating
    * Number of Reviews
    * Reviews (Review date, review text, review ratings, reviewer name)
    * Specification (weight, crystal, case, and band materials, water resistance depth)
    * Stock Status
    * Product Specifications
    * Product Image URL

2. Database: PostgreSQL is used to store the scraped product data in a structured format, enabling efficient querying.

3. API: A FastAPI-based REST API to:
    * Query products with search, filter, and sort functionalities.
    * Retrieve detailed product reviews with pagination support.
    * Fetch the top-rated products based on rating and number of reviews.

4. LLM-Based Conversational Agent: An AI agent that uses the scraped data to provide insights and answer user queries.

# Project Structure
```
watch-scraper-llm
├── scraper                  # Scraper folder
│   ├── __init__.py          # Initializes the scraper package
│   ├── dbconnection.py      # Database connection utilities
│   ├── scraper_utils.py     # Helper functions for scraping
├── fastapi_app.py           # Main FastAPI application
├── scraper.py               # Selenium-based scraper script
├── models.py                # Pydantic models for API responses
├── requirements.txt         # Python dependencies
├── Dockerfile               # Dockerfile for FastAPI app
├── docker-compose.yml       # Docker Compose configuration
├── README.md                # Project documentation
└── .env                     # Environment variables file
```

# Database Schema
```sql
CREATE TABLE IF NOT EXISTS watches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    brand VARCHAR(255),
    model VARCHAR(255),
    price DECIMAL(10, 2),
    specifications JSONB,
    rating DECIMAL(3, 2),
    reviews JSONB,
    n_rating INTEGER,
    stock TEXT,
    image_url TEXT,
    scraped_at TIMESTAMP
);

```

# Running on Local
### Cloning the Repository
Clone this repository using
```bash
git clone https://github.com/hasu234/watch-scraper-llm.git
```
Go to the project Directory
```bash
cd watch-scraper-llm
```
### Environment Variables

Create a `.env` file in the project directory with the following variables:

```plaintext
DB_HOST=localhost
DB_PORT=5432
DB_NAME=scraper
DB_USER=postgres
DB_PASSWORD=password
```
### Creating Conda Environment
```bash 
conda create -n scraper python=3.10
conda activate scraper
```
### Installing Requirements
```bash
pip install -r requirements.txt
```
### Running the Scrapper
Run the ```scraper.py``` file using
```bash
python scrappr.py
```
The scraper would scrape product (watch) info from ```https://www.amazon.in/``` website. Firstly the script will scrape _product page link_ for 5 search pages which is defined in [here](https://github.com/hasu234/watch-scraper-llm/blob/873844f875f1be4856cf219cffeef833588f9bb5/scraper/scraper_utils.py#L36). Then iterate through the link to scrape required data from the webpage. Finally, it will direcly insert the data to the PostgreSQL database if the database connection is configured.

The ```scraper.py``` has a scheduled_scrape function which would schedule the scrapping for a specific time interval (1 hours for our case) which is define [here](https://github.com/hasu234/watch-scraper-llm/blob/873844f875f1be4856cf219cffeef833588f9bb5/scraper.py#L98). 

The console log should report ```Data inserted successfully!``` if everything went good. 

## Running the FastAPI application
Run the ```fastapi_app.py``` using 
```bash
uvicorn fastapi_app:app
```
It would start running on ```localhost:8000``` or ```127.0.0.1:8000``` port. 

# Running on Docker
## Run the Dockerized Application
Before starting with docker, make sure the docker daemon is running.

### Building the docker Images (First time only)
```
docker-compose up --build
```
### Running the prebuilt Images
```
docker-compose up
```
The application should run on the console. Two separate images should run on a single container. One for ```postgresql``` on ```localhost:5432``` port (pgAdmin will be accessible on port ```localhost:5050```)  and another for the `FastAPI` app on ```localhost:8000``` port. 

N.B. The scraper script is not dockerized as it required some time to scrap the data. I would design another API which would do the scraping automatically for other products and custom search page length.

### Stopping the prebuilt Images
```
docker-compose down
```

# API Endpoints
### Base URL
```bash
http://localhost:8000
```

### 1. Get Products
**Endpoint:** `GET http://localhost:8000/products`

**Description:** 
Retrieve a list of products (watches) from the database with optional filtering, sorting, and pagination.

**Query Parameters:**
- `brand` (Optional): Filter products by brand (e.g., `Casio`).
- `model` (Optional): Filter products by model (e.g., `G-Shock`).
- `min_price` (Optional): Filter products with a price greater than or equal to this value.
- `max_price` (Optional): Filter products with a price less than or equal to this value.
- `min_rating` (Optional): Filter products with a rating greater than or equal to this value.
- `sort_by` (Optional, Default: `price`): The field to sort the results by. Options: `price`, `rating`.
- `order` (Optional, Default: `asc`): The sorting order. Options: `asc` (ascending), `desc` (descending).
- `page` (Optional, Default: `1`): The page number for pagination.
- `limit` (Optional, Default: `10`): The number of items per page.

**Response:**
- **200 OK:** Returns a list of `Product` objects.
- **400 Bad Request:** If `sort_by` is not valid.
- **404 Not Found:** If no products are found.
- **500 Internal Server Error:** If there is an error processing the request.

**Example Request:**
```http
GET http://localhost:8000/products?brand=Casio&min_price=50&sort_by=rating&order=desc&page=1&limit=5
```
**Example Response:** 
```json
[
  {
    "id": 184,
    "name": "Sounce Premium Silicone Adjustable Watch Band Waterproof, Durable, Comfortable, Sporty Strap Replacement Lightweight for Xiaomi Mi Band 5/ Mi Band 6 (Not Compatible For Mi Band 1/2/3/4)-(Black & Blue)",
    "brand": "Sounce",
    "model": null,
    "price": 129,
    "specifications": {
      "item_weight": "70 g",
      "band_material": null,
      "case_material": null,
      "crystal_material": null,
      "water_resistant_depth": null
    },
    "rating": 4,
    "n_rating": 5698,
    "stock": "In stock",
    "image_url": "https://m.media-amazon.com/images/I/61tdO4yvAOL._SX679_.jpg",
    "scraped_at": "2024-10-21T13:05:47.122625"
  },
  {
    "id": 6,
    "name": "6 Colours Luminous LED Display Fashionable Children Kids Digital Watches Waterproof Sports Square Electronic Led Watch for Kids Boy Baby Girls Digital Watch for Kids",
    "brand": "Acnos",
    "model": "EARTH-BLACK-LED",
    "price": 149,
    "specifications": {
      "item_weight": "30 g",
      "band_material": "Polyurethane",
      "case_material": "PU",
      "crystal_material": "PU",
      "water_resistant_depth": "30 Millimeters"
    },
    "rating": 4,
    "n_rating": 1112,
    "stock": "In stock",
    "image_url": "https://m.media-amazon.com/images/I/61ohjb-5f5L._SX679_.jpg",
    "scraped_at": "2024-10-21T13:05:47.115614"
  },
  ...
]
```
### 2. Get Top Products
**Endpoint:** `GET http://localhost:8000/products/top`

**Description:**  
This endpoint retrieves the top products from the database based on their rating and the number of reviews.

**Response:**
- **200 OK:** Returns a list of top products, each represented by a `TopProduct` object.
- **404 Not Found:** If no top products are found in the database.
- **500 Internal Server Error:** If there is an error processing the request.

**Example Request:**
```http
GET http://127.0.0.1:8000/products/top
```

**Response Example:** Retrieve the top 10 products from the database based on their rating and number of ratings.
```json
[
  {
    "id": 272,
    "name": "Multifunction Watch for Men - Perfect Blend of Style and Utility” | Water Resistant Square dial Unique Design Wrist Watch for Man | Best Gift for Males",
    "rating": 5,
    "n_rating": 1,
    "reviews": [
      {
        "Review Date": "Reviewed in India on 2 October 2024",
        "Review Text": "AS IN THE PICTURE AWESOME WATCH PREMIUM QUALITY EVERYTHING IS WORKING SUPPERB QUALITY",
        "Review Rating": "5.0",
        "Reviewer Name": "GAUTAM ABRAHAM SUNARIA"
      }
    ]
  },
  {
    "id": 335,
    "name": "Poze Quartz Analog Grey Dial Stainless Steel Strap Watch for Men-SP70020QM03W",
    "rating": 5,
    "n_rating": 1,
    "reviews": [
      {
        "Review Date": "Reviewed in India on 7 September 2024",
        "Review Text": "Good Buy",
        "Review Rating": "5.0",
        "Reviewer Name": "sathish"
      }
    ]
  },
  ...
]
```

### 3. Get Product Reviews

**Endpoint:** `GET http://127.0.0.1:8000/products/{product_id}/reviews`

**Description:**  
This endpoint retrieves reviews for a specific product identified by its `product_id`. The response includes pagination to manage the number of reviews returned.

#### Path Parameters

- **`product_id`** (integer):  
  The unique identifier of the product for which reviews are being retrieved.

#### Query Parameters

- **`page`** (integer, optional, default: `1`):  
  The page number to retrieve. Must be greater than or equal to 1.

- **`limit`** (integer, optional, default: `10`):  
  The maximum number of reviews to return per page. Must be greater than or equal to 1.


**Example Request:**
```http
GET http://127.0.0.1:8000/products/315/reviews?page=1&limit=5
```

**Example Response:** Returns a list of reviews for the specified product.
```json
[
  {
    "Review Date": "Reviewed in India on 12 September 2020",
    "Review Text": "Awesome everyday watch.",
    "Review Rating": "4.0",
    "Reviewer Name": "Alto"
  },
  {
    "Review Date": "Reviewed in the United States on 12 September 2024",
    "Review Text": "Beautiful!",
    "Review Rating": "5.0",
    "Reviewer Name": "Michelle A."
  },
  {
    "Review Date": "Reviewed in the United States on 16 January 2024",
    "Review Text": "I like the style and size of the watch. I love the watchband thats leather with plenty of holes so it will fit from large to small wrists!",
    "Review Rating": "5.0",
    "Reviewer Name": "crystal mcrae"
  },
  {
    "Review Date": "Reviewed in the United States on 12 September 2024",
    "Review Text": "Pretty",
    "Review Rating": "5.0",
    "Reviewer Name": "Amazon Customer"
  },
  {
    "Review Date": "Reviewed in Mexico on 16 January 2024",
    "Review Text": "Es muy bonito y combina con cualquier atuendo, fue un regalo y le encantó a la persona",
    "Review Rating": "5.0",
    "Reviewer Name": "Jairo Flores"
  }
]
```

## Logging
The application logs various events and errors. Logs are available in the console output where the application is running.
