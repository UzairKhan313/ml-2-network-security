from pymongo import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException
import os
from dotenv import load_dotenv

MONGODB_URI = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    logger.logging.info(
        "Pinged your deployment. You successfully connected to MongoDB!"
    )
except Exception as e:
    raise NetworkSecurityException("Unable to connect to MongoDB", e)
