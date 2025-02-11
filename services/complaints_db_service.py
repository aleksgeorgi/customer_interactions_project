from models.db_connection import get_db
from flask import jsonify, request
from bson import ObjectId
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

db = get_db()
collection = db["complaints"]

def get_complaints_from_db(company: str):
    try:
        if not company:
            raise ValueError("Company name is required")
        
        # Limit the number of complaints returned to 3
        complaints = list(collection.find({"Company": company}, {"_id": 0}).limit(3))
        
        if not complaints:
            return jsonify({"message": "No complaints found for the specified company."}), 404
        
        logger.info(f"Found {len(complaints)} complaints for {company}")
        return jsonify(complaints), 200 
    except ValueError as ve:
        logger.error(f"ValueError in get_complaints_from_db: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in get_complaints_from_db: {e}")
        return jsonify({"error": "Internal Server Error"}), 500 
    
def add_complaint_to_db():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    complaint = request.get_json()
    
    # Validate required fields
    required_fields = ["Company", "Issue", "Description"]
    if not all(field in complaint for field in required_fields):
        logger.error(f"Missing required fields. Required fields are: {required_fields}")
        return jsonify({
            "error": f"Missing required fields. Required fields are: {required_fields}"
        }), 400
    
    # Add timestamp and generate ID if not provided
    complaint['_id'] = str(ObjectId())
    
    try:
        collection.insert_one(complaint)
        logger.info(f"Complaint added successfully! ID: {complaint['_id']}")
        return jsonify({
            "message": "Complaint added successfully!",
            "complaint_id": complaint['_id']
        }), 201
    except Exception as e:
        logger.error(f"Error in add_complaint_to_db: {e}")
        return jsonify({"error": str(e)}), 500
    
def update_complaint(complaint_id: str):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    updated_data = request.get_json()
    
    try:
        # Convert the complaint_id to ObjectId
        result = collection.update_one(
            {"_id": ObjectId(complaint_id)},  # Convert string ID to ObjectId
            {"$set": updated_data}
        )
        
        if result.matched_count:
            logger.info(f"Complaint updated successfully! ID: {complaint_id}")
            return jsonify({"message": "Complaint updated successfully!"})
        else:
            logger.error(f"Complaint not found. ID: {complaint_id}")
            return jsonify({"message": "Complaint not found."}), 404
    except Exception as e:
        logger.error(f"Error in update_complaint: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    # Test get_complaints_from_db function
    test_company = "Test Company"
    response = get_complaints_from_db(test_company)
    print(response)
