import yaml
import os, sys
import numpy as np
import dill
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_arr(file_path, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_object:
            np.save(file_object, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path, obj: object):
    try:
        logging.info("Enter the Save object method of main utils. ")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_object:
            pickle.dump(obj, file_object)

        logging.info("Exit the Save object method of main utils. ")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
