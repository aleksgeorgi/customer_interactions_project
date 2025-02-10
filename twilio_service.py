from dotenv import load_dotenv
import os
from twilio.rest import Client
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

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

if __name__ == "__main__":
    send_sms("+18777804236", "Hello, this is a test message from Twilio!")
