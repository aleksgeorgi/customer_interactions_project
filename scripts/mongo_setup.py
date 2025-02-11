import pandas as pd
from models.db_connection import get_db
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

"""Populates the MongoDB database with the complaints data from the CSV file."""
try:
    db = get_db()
    collection = db["complaints"]

    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv("data/complaints-2025.csv")

    # Convert DataFrame rows to dictionary format for MongoDB insertion
    records = df.to_dict(orient="records")

    # Insert data into MongoDB collection
    collection.insert_many(records)

    logger.info(f"✅ Inserted {len(records)} complaints into MongoDB!")
except FileNotFoundError as fnf_error:
    logger.error(f"❌ FileNotFoundError: {fnf_error}")
except pd.errors.EmptyDataError as ede_error:
    logger.error(f"❌ EmptyDataError: {ede_error}")
except pd.errors.ParserError as pe_error:
    logger.error(f"❌ ParserError: {pe_error}")
except Exception as e:
    logger.error(f"❌ An error occurred: {e}")
