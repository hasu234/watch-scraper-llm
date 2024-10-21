
import os
import time
import json
import random
import schedule
import psycopg2
import logging
from datetime import datetime
from dotenv import load_dotenv
from scraper import scrape_amazon
from psycopg2.extras import execute_values


# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to connect to PostgreSQL using environment variables
def connect_to_db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

# Function to create the table if it doesn't exist
def create_table_if_not_exists():
    conn = connect_to_db()
    cur = conn.cursor()

    # SQL query to create the table if it doesn't exist
    create_table_query = """
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
    """

    cur.execute(create_table_query)  # Execute the query to create the table
    conn.commit()  # Save changes
    cur.close()  # Close the cursor
    conn.close()  # Close the connection

def insert_data(name, brand, model, price, specifications, rating, reviews, n_rating, stock, image):
    # Create the table if it doesn't exist
    create_table_if_not_exists()

    conn = connect_to_db()

    # Insert query for batch insert
    query = """
    INSERT INTO watches (name, brand, model, price, specifications, rating, reviews, n_rating, stock, image_url, scraped_at)
    VALUES %s
    """

    # Zip the data together, convert specifications and reviews to JSON
    data = [
        (name[i], brand[i], model[i], price[i], json.dumps(specifications[i]), rating[i], json.dumps(reviews[i]), n_rating[i], stock[i], image[i], datetime.now())
        for i in range(len(name))
    ]
    print("Inserting data...")

    try:
        # Open a cursor to perform database operations
        with conn.cursor() as cursor:
            # Perform batch insert
            execute_values(cursor, query, data)
            conn.commit()  # Commit the transaction
            print("All data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        conn.close()  # Close the connection


# Function to run the scraper at intervals
def scheduled_scrape():
    # List of watch URLs to scrape (you can dynamically generate or read from a file)
    item = "watch"
    # logger.info(f"Scraping Amazon for {item}")
    name, brand, model, price, specifications, rating, reviews, n_rating, stock, image = scrape_amazon(item)

    insert_data(name, brand, model, price, specifications, rating, reviews, n_rating, stock, image)  # Insert the scraped data into

    time.sleep(random.randint(5, 15))  # Random delay to avoid bot detection

# Schedule the scraping task (run every hour for example)
schedule.every(1).hours.do(scheduled_scrape)

# Run the scrape function immediately before scheduling
scheduled_scrape()

# Main loop to keep the script running
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
