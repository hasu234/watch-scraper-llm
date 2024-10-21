from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
from scraper import connect_to_db

# FastAPI app instance
app = FastAPI()

# Product model for response
class Product(BaseModel):
    id: int
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    price: Optional[float] = None
    specifications: Optional[Dict] = None
    rating: Optional[float] = None
    # reviews: Optional[List[Dict]] = None
    n_rating: Optional[int] = None
    stock: Optional[str] = None
    image_url: Optional[str] = None
    scraped_at: str

# TopProduct model for top products response
class TopProduct(BaseModel):
    id: int
    name: Optional[str] = None
    rating: Optional[float] = None
    n_rating: Optional[int] = None
    reviews: Optional[List[Dict]] = None

# Endpoint to get products with search, filter, sort, and pagination
@app.get("/products", response_model=List[Product])
def get_products(
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_rating: Optional[float] = Query(None),
    sort_by: Optional[str] = Query('price'),  # Sorting criteria (price, rating)
    order: Optional[str] = Query('asc'),  # Sorting order ('asc' or 'desc')
    page: int = Query(1, ge=1),  # Page number
    limit: int = Query(10, ge=1)  # Number of items per page
):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Base query
        query = "SELECT * FROM watches WHERE TRUE"

        # Adding search filters
        if brand:
            query += f" AND brand ILIKE '%{brand}%'"
        if model:
            query += f" AND model ILIKE '%{model}%'"

        # Adding price range filter
        if min_price is not None:
            query += f" AND price >= {min_price}"
        if max_price is not None:
            query += f" AND price <= {max_price}"

        # Adding rating filter
        if min_rating is not None:
            query += f" AND rating >= {min_rating}"

        # Sorting logic
        if sort_by in ['price', 'rating']:
            query += f" ORDER BY {sort_by} {order.upper()}"
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by value")

        # Pagination
        offset = (page - 1) * limit
        query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query)
        products = cursor.fetchall()

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        # Convert result set to list of Product instances
        result_list = []
        for prod in products:
            product = Product(
                id=prod[0],
                name=prod[1],
                brand=prod[2],
                model=prod[3],
                price=float(prod[4]) if prod[4] is not None else None,
                specifications=prod[5],
                rating=float(prod[6]) if prod[6] is not None else None,
                # reviews=prod[7],
                n_rating=prod[8],
                stock=prod[9],
                image_url=prod[10],
                scraped_at=prod[11].isoformat()  # Convert datetime to string
            )
            result_list.append(product)

        return result_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()


# Endpoint to get top products based on rating and number of reviews
@app.get("/products/top", response_model=List[TopProduct])
def get_top_products():
    try:
        conn = connect_to_db()  # Replace with your actual database connection function
        cursor = conn.cursor()
        query = """
        SELECT *
        FROM watches
        WHERE rating IS NOT NULL
        ORDER BY rating DESC, n_rating DESC
        LIMIT 10;
        """
        cursor.execute(query)
        top_products = cursor.fetchall()

        if not top_products:
            raise HTTPException(status_code=404, detail="No top products found")

        # Convert the fetched tuples into Product instances
        products = []
        for result in top_products:
           product = TopProduct(
                id=result[0],
                name=result[1] if result[1] is not None else None,
                rating=float(result[6]) if result[6] is not None else None,  # Allow rating to be None
                n_rating=result[8] if result[8] is not None else 0,  # Default n_rating to 0 if None
                reviews=result[7] if result[7] is not None else [],  # Use empty list if None
            )
           
           products.append(product)

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        cursor.close()


@app.get("/products/{product_id}/reviews", response_model=List[Dict])
def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),  # Default to page 1, must be >= 1
    limit: int = Query(10, ge=1)  # Default to 10 reviews per page, must be >= 1
):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # SQL query for retrieving reviews of a specific product with pagination
        offset = (page - 1) * limit
        query = """
        SELECT reviews 
        FROM watches
        WHERE id = %s
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Product not found")

        reviews = result[0]

        # If no reviews are found, return an empty list
        if reviews is None:
            return []

        # Paginate the reviews (assuming reviews is a list)
        paginated_reviews = reviews[offset:offset + limit]

        return paginated_reviews

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        cursor.close()
        conn.close()

