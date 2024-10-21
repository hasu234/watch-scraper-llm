from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from scraper import connect_to_db

# FastAPI app instance
app = FastAPI()

# Product model for response
class Product(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    price: float
    specifications: dict
    rating: Optional[float] = None
    reviews: Optional[dict] = None
    n_rating: int
    stock: str
    image_url: str
    scraped_at: str

# Review model for reviews response
class Review(BaseModel):
    reviews: dict

# Endpoint to get products with search, filter, sort, and pagination
@app.get("/products", response_model=List[Product])
def get_products(
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_rating: Optional[float] = Query(None),
    sort_by: Optional[str] = Query('price'),
    order: Optional[str] = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT * FROM watches WHERE TRUE"
        
        # Search and filtering logic
        if brand:
            query += f" AND brand ILIKE '%{brand}%'"
        if model:
            query += f" AND model ILIKE '%{model}%'"
        if min_price:
            query += f" AND price >= {min_price}"
        if max_price:
            query += f" AND price <= {max_price}"
        if min_rating:
            query += f" AND rating >= {min_rating}"

        # Sorting
        query += f" ORDER BY {sort_by} {order.upper()}"

        # Pagination
        offset = (page - 1) * limit
        query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query)
        products = cursor.fetchall()

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Endpoint to get top products based on rating and number of reviews
@app.get("/products/top", response_model=List[Product])
def get_top_products():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
        SELECT * FROM watches 
        ORDER BY rating DESC, n_rating DESC
        LIMIT 10
        """
        cursor.execute(query)
        top_products = cursor.fetchall()

        if not top_products:
            raise HTTPException(status_code=404, detail="No top products found")

        return top_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Endpoint to get all reviews for a specific product with pagination
@app.get("/products/{product_id}/reviews", response_model=List[Review])
def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        offset = (page - 1) * limit

        # Get reviews for the product with pagination
        query = """
        SELECT reviews FROM watches 
        WHERE id = %s
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (product_id, limit, offset))
        reviews = cursor.fetchall()

        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for this product")

        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

