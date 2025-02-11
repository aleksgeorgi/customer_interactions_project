from flask import Flask, jsonify, request
from services.twilio_voice_service import receive_call
from services.numbers_db_service import add_phone_number_to_db
from services.complaints_db_service import get_complaints_from_db, add_complaint_to_db, update_complaint
from services.twilio_sms_service import send_notification_service
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/complaints/<company>", methods=["GET"])
def get_complaints(company):
    """Fetch complaints for a given company.
    USE:
        Invoke-RestMethod -Uri "http://localhost:5000/complaints/MOHELA" -Method Get
    """
    try:
        return get_complaints_from_db(company)
    except Exception as e:
        app.logger.error(f"Error in get_complaints route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/complaints", methods=["POST"])
def add_complaint():
    """Add a new complaint
    USE:
        Invoke-RestMethod -Uri "http://localhost:5000/complaints" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"Company": "AleksCorp", "Issue": "Billing error", "Description": "Unexpected charge on account"}'
    
    """
    try:
        return add_complaint_to_db()
    except ValueError as ve:
        app.logger.error(f"ValueError in add_complaint route: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error in add_complaint route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/complaints/<complaint_id>", methods=["PUT"])
def update_complaint(complaint_id):
    """Update an existing complaint.
    USE:
        $complaintId = "679c16f8cf4944fca50b01d0"  
        $updateData = @{
            "Issue" = "Updated Issue"
            "Description" = "Updated Description"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5000/complaints/$complaintId" -Method Put -ContentType "application/json" -Body $updateData
    """
    try:
        return update_complaint(complaint_id)
    except ValueError as ve:
        app.logger.error(f"ValueError in update_complaint route: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error in update_complaint route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route("/send-notification", methods=["POST"])
def send_notification():
    """Endpoint to trigger SMS notification.
    USE:
        $uri = "https://api.twilio.com/2010-04-01/Accounts/$env:TWILIO_ACCOUNT_SID/Messages.json"
        $body = @{
            To = '+18777804236'
            From = $env:TWILIO_PHONE_NUMBER
            Body = 'This is a message from twilio!'
        }
        $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:TWILIO_ACCOUNT_SID:$env:TWILIO_AUTH_TOKEN"))

        $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType 'application/x-www-form-urlencoded' -Headers @{Authorization=("Basic {0}" -f $auth)}

        $response
    
    """
    try:
        return send_notification_service()
    except Exception as e:
        app.logger.error(f"Error in send-notification route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Endpoint to receive phone calls.
    USE:
        from an external phone call the twilio number
    """
    try:
        return receive_call()
    except Exception as e:
        app.logger.error(f"Error in voice route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/phone-numbers", methods=["POST"])
def add_phone_number():
    """Add a new phone number to the phone_numbers collection.
    USE:
        $uri = "http://localhost:5000/phone-numbers"
        $body = @{
            PhoneNumber = "+1234567890"
            Name = "John Doe"
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType 'application/json'

        $response
    
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    
    try:
        # Call the service function with the data
        add_phone_number_to_db(data)
        return jsonify({"message": "Phone number added successfully!"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error adding phone number: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # host="0.0.0.0":  makes the server accessible from any network interface, not just localhost, particularly useful when running the app inside a Docker container, as it allows external access to the app.
    # Setting host="0.0.0.0" is crucial when running the app in a Docker container. It ensures that the app is accessible from outside the container, allowing you to map the container's port to a port on your host machine
    # port=5000:  specifies the port on which the Flask app will run.
