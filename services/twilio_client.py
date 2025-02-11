import os
from twilio.rest import Client
from dotenv import load_dotenv
from utils.logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()

def get_twilio_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN") 
    try:
        return Client(account_sid, auth_token)
    except Exception as e:
        logger.error(f"❌ An error occurred while creating the Twilio client: {e}")
        raise

if __name__ == "__main__":
    client = get_twilio_client()
    logger.info(client)
