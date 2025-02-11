from models.db_connection import get_db
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

db = get_db()

# new phone_numbers collection
phone_numbers_collection = db["phone_numbers"]

def add_phone_number_to_db(data: dict):
    """Add a new phone number to the phone_numbers collection."""
    phone_number = data.get("phone_number")
    name = data.get("name")
    
    try:
        # Ensure both fields are provided
        if not phone_number or not name:
            raise ValueError("Both phone_number and name are required")
        
        phone_numbers_collection.insert_one({"name": name, "phone_number": phone_number})
        logger.info(f"✅ Added phone number {phone_number} for {name} to MongoDB!")
    except ValueError as ve:
        logger.error(f"❌ ValueError: {ve}")
        raise
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        raise

def get_list_of_all_phone_numbers_from_db():
    """Retrieve all phone numbers from the phone_numbers collection."""
    try:
        phone_numbers = list(phone_numbers_collection.find({}, {"_id": 0}))
        return phone_numbers
    except Exception as e:
        logger.error(f"❌ An error occurred while retrieving phone numbers: {e}")
        raise

def get_record_by_phone_number_from_db(phone_number: str):
    """Retrieve a record by phone number from the phone_numbers collection."""
    try:
        record = phone_numbers_collection.find_one({"phone_number": phone_number}, {"_id": 0})
        return record
    except Exception as e:
        logger.error(f"❌ An error occurred while retrieving the record for phone number {phone_number}: {e}")
        raise

if __name__ == "__main__":

    # Get all phone numbers
    numbers = get_list_of_all_phone_numbers_from_db()
    logger.info("📞 Phone Numbers in Database:")
    for number in numbers:
        logger.info(number)