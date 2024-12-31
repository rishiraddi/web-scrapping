import selenium
from selenium import webdriver
from pymongo import MongoClient
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from pymongo.errors import PyMongoError

# Initialize Selenium webdriver
driver = webdriver.Chrome()

# Use ProxyMesh to get a new IP address for each request
proxy_url = f"http://rishiraddi:Rishi%40123@proxymesh.com"
driver.proxy = {"http": proxy_url, "https": proxy_url}

# Navigate to X homepage
driver.get("https://x.com/i/flow/login")

try:
    # Improved element locators (replace if necessary)
    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "text"))
    )
    username_field.send_keys("Rishi8217341586")

    next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button'].r-1phboty"))
    )
    next_button.click()


    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )
    password_field.send_keys("Rishi@18081979")

    # Submit the login form (if applicable)
    # ... (Handle login form submission if needed)

    # Navigate to explore page
    driver.get("https://x.com/explore/tabs/trending")

    # Find trending topics (adjust CSS selector as needed)
    trending_topics_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-175oi2rcss-175oi2r r-f8sm7e r-13qz1uu")) 
    )

    trending_topics_text = [topic.text for topic in trending_topics_elements[:5]]

    # Create a unique ID for this scrape
    unique_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Connect to MongoDB database
    client = MongoClient()
    db = client["trending"]

    # Check if collection exists
    if "trends" in db.list_collection_names():
        collection = db["trends"] 
    else:
        print("Creating 'trends' collection...")
        collection = db.create_collection("trends", {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["unique_id", "trend1", "trend2", "trend3", "trend4", "trend5", "date_time", "ip_address"],
                    "properties": {
                        "unique_id": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "trend1": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "trend2": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "trend3": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "trend4": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "trend5": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "date_time": {
                            "bsonType": "string", 
                            "description": "must be a string and is required"
                        },
                        "ip_address": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        }
                    }
                }
            }
        })

    # Check if document with the same unique_id already exists
    existing_document = collection.find_one({"unique_id": unique_id})

    if existing_document is None:
        # Store the results in MongoDB only if it doesn't exist
        document = {
            "unique_id": unique_id,
            "trend1": trending_topics_text[0],
            "trend2": trending_topics_text[1],
            "trend3": trending_topics_text[2],
            "trend4": trending_topics_text[3],
            "trend5": trending_topics_text[4],
            "date_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ip_address": driver.proxy["http"].split(":")[1]
        }
        collection.insert_one(document)
        print(f"Document with unique_id: {unique_id} inserted successfully.")
    else:
        print(f"Document with unique_id: {unique_id} already exists.")

except (NoSuchElementException, TimeoutException, WebDriverException, PyMongoError) as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

print("Script execution completed.")