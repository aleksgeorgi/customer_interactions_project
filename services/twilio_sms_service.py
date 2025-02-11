from flask import jsonify, request
import os
from dotenv import load_dotenv
from services.twilio_client import get_twilio_client
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

load_dotenv()
client = get_twilio_client()
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_sms(to_numer: str, message_body: str):
    """Send an SMS message using Twilio."""
    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body=message_body,
            to=to_numer
        )
        logger.info(f"SMS sent successfully to {to_numer}. SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending SMS to {to_numer}: {str(e)}")
        return None
    
def send_notification_service():
    try:
        data = request.get_json()
        to_number = data.get("to_number")
        message_body = data.get("message_body")
        
        logger.info(f"Sending SMS to {to_number} with message: {message_body}")
        
        if not to_number or not message_body:
            return jsonify({"error": "Missing required parameters"}), 400
        
        message_sid = send_sms(to_number, message_body)
        
        if message_sid:
            return jsonify({"message": "SMS notification sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to send SMS notification. " + str(e)}), 500
    
if __name__ == "__main__":
    # send_sms("+18777804236", "Hello, this is a test message from Twilio!")
    # send_notification_service()
    pass