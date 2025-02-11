from dotenv import load_dotenv
from flask import request
import os
from twilio.twiml.voice_response import VoiceResponse
from services.numbers_db_service import get_record_by_phone_number_from_db 
from services.twilio_client import get_twilio_client
from utils.logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()
client = get_twilio_client()
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
    
def make_call(to_number: str):
    """Make a phone call using Twilio and Twiml"""
    try:
        call = client.calls.create(
            twiml="<Response><Say>Hello, this is a test call from Aleksandra's Twilio test phone number. Have a good day!</Say></Response>",
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            # url="https://demo.twilio.com/docs/voice.xml"
        )
        logger.info(f"Call made successfully to {to_number}. SID: {call.sid}")
        return call.sid

    except Exception as e:
        logger.error(f"Error making call to {to_number}: {str(e)}")
        return None

def make_call():
    """Make a phone call using Twilio and Twiml"""
    data = request.get_json()
    to_number = data.get("to_number")
    try:
        call = client.calls.create(
            twiml="<Response><Say>Hello, this is a test call from Aleksandra's Twilio test phone number. Have a good day!</Say></Response>",
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            # url="https://demo.twilio.com/docs/voice.xml"
        )
        logger.info(f"Call made successfully to {to_number}. SID: {call.sid}")
        return call.sid

    except Exception as e:
        logger.error(f"Error making call to {to_number}: {str(e)}")
        return None

def receive_call():
    response = VoiceResponse()
    
    try:
        # Get the caller's phone number from the request
        caller_number = request.values.get("From")
        
        if not caller_number:
            raise ValueError("Caller number is missing from the request.")
        
        # Retrieve the caller's record from the database
        caller_record = get_record_by_phone_number_from_db(caller_number)
        
        # Customize the message based on the caller's information
        if caller_record:
            caller_name = caller_record.get("name")
            if caller_name == "James Hackland":
                response.say(f"Hello, {caller_name}! Aleks wants you to know you're a baddass with a tight ass! Hope you are entertained by this call.")
            elif caller_name == "Shirmela Rambally":
                response.say(f"Hello, {caller_name}! Aleks wants you to know you will always be her littel panda bear. Love, your gazelle.")
            else:
                response.say(f"Hello, {caller_name}! You are special enough to be in my database. Hope you are entertained by this call.")
        else:
            response.say("Hello, you've reached Aleksandra's Twilio test phone number. Have a good day!")
    
    except ValueError as ve:
        logger.error(f"ValueError in receive_call: {ve}")
        response.say("There was an error processing your call. Please try again later.")
    except Exception as e:
        logger.error(f"Error in receive_call: {e}")
        response.say("An unexpected error occurred. Please try again later.")
    
    return str(response)


if __name__ == "__main__":
    # send_sms("+18777804236", "Hello, this is a test message from Twilio!")
    make_call(MY_PHONE_NUMBER)
