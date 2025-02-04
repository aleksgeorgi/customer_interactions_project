from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["customer_support"]
collection = db["complaints"]

@app.route("/complaints/<company>", methods=["GET"])
def get_complaints(company):
    """Fetch complaints for a given company."""
    try:
        complaints = list(collection.find({"Company": company}, {"_id": 0}))  # Exclude MongoDB ID
        return jsonify(complaints), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route("/complaints", methods=["POST"])
def add_complaint():
    """Add a new complaint."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    complaint = request.get_json()
    
    # Validate required fields
    required_fields = ["Company", "Issue", "Description"]
    if not all(field in complaint for field in required_fields):
        return jsonify({
            "error": f"Missing required fields. Required fields are: {required_fields}"
        }), 400
    
    # Add timestamp and generate ID if not provided
    complaint['_id'] = str(ObjectId())
    
    try:
        collection.insert_one(complaint)
        return jsonify({
            "message": "Complaint added successfully!",
            "complaint_id": complaint['_id']
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/complaints/<complaint_id>", methods=["PUT"])
def update_complaint(complaint_id):
    """Update an existing complaint."""
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
            return jsonify({"message": "Complaint updated successfully!"})
        else:
            return jsonify({"message": "Complaint not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # host="0.0.0.0":  makes the server accessible from any network interface, not just localhost, particularly useful when running the app inside a Docker container, as it allows external access to the app.
    #  Setting host="0.0.0.0" is crucial when running the app in a Docker container. It ensures that the app is accessible from outside the container, allowing you to map the container's port to a port on your host machine
    # port=5000:  specifies the port on which the Flask app will run.
