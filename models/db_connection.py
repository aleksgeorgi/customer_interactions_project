from pymongo import MongoClient
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

def get_db():
   """ Connect to MongoDB (Docker service name: "mongo")"""
   client = MongoClient("mongodb://mongo:27017/")
   db = client["customer_support"]
   logger.info("Connected to MongoDB")
   return db
