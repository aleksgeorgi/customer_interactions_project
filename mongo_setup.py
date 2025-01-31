import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB (Docker service name: "mongo")
client = MongoClient("mongodb://mongo:27017/")  
db = client["customer_support"]
collection = db["complaints"]

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("data/complaints-2025.csv")

# Convert DataFrame rows to dictionary format for MongoDB insertion
records = df.to_dict(orient="records")

# Insert data into MongoDB collection
collection.insert_many(records)

print(f"✅ Inserted {len(records)} complaints into MongoDB!")
