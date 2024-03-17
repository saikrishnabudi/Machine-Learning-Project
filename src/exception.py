import sys
from types import TracebackType
from src.logger import logging


def error_message_detail(error, error_detail: sys): # type: ignore
    _, _, exc_tb = error_detail.exc_info()
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
            file_name, exc_tb.tb_lineno, str(error)
        )
    else:
        error_message = str(error)
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):  # type: ignore
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 10
    except Exception as e:
        logging.info("Divided by zero")
        raise CustomException(e, sys)

        
