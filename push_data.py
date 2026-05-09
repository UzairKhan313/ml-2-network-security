import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

import certifi

ca = certifi.where()
import pandas as pd
import numpy as np
from pymongo import MongoClient

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


class NetworkDataExtractor:
    def __init__(self, uri: str):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException("Unable to connect to MongoDB", sys)

    def convert_csv_to_json(self, csv_file_path: str) -> str:
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(drop=True, inplace=True)
            records = json.loads(df.T.to_json()).values()
            records = list(records)

            logging.info("Successfully converted CSV to JSON")
            return records
        except Exception as e:
            raise NetworkSecurityException("Error converting CSV to JSON", sys)

    def insert_data_to_mongodb(self, data: list, db_name: str, collection_name: str):
        try:
            self.db_name = db_name
            self.collection_name = collection_name
            self.data = data

            self.mongodb_client = MongoClient(MONGODB_URI)
            self.db_name = self.mongodb_client[self.db_name]
            self.collection_name = self.db_name[self.collection_name]
            self.collection_name.insert_many(self.data)
            return len(self.data)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE_NAME = "network_security"
    COLLECTION_NAME = "Network_data"

    network_obj = NetworkDataExtractor(MONGODB_URI)
    records = network_obj.convert_csv_to_json(FILE_PATH)
    no_of_records_inserted = network_obj.insert_data_to_mongodb(
        records, DATABASE_NAME, COLLECTION_NAME
    )

    logging.info(f"Successfully inserted {no_of_records_inserted} records into MongoDB")
