import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv() 

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")


# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.get_database("slide_generator")  # Creates database if not exists
slides_collection = db.slides  # Creates collection if not exists


# Create document to save
slide_document = {
    "topic": "topic",
    "description": "description",
    "slides": "all_slides",
    "created_at": datetime.utcnow(),
    "metadata": {
        "slide_count": "all_slides",
        "app_version": "1.0"
    }
}

# Insert into MongoDB
result = slides_collection.insert_one(slide_document)
print(f"Inserted document with ID: {result.inserted_id}")