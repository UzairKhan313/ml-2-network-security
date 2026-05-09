import sys
from networksecurity.logging import logger


class NetworkSecurityException(Exception):
    def __init__(self, message: str, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in python script name [{0}] line number [{1}] and error message is [{2}]".format(
            self.file_name, self.line_number, self.message
        )
