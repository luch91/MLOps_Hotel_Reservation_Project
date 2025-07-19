from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_number(a, b):
    try:
        logger.info("Dividing {} by {}".format(a, b))
        result = a / b
        return result
    except Exception as e:
        logger.error("An exception occurred during division")
        raise CustomException(str(e), sys)


# raise CustomException(f"An error occurred: {e}", sys)  # Raise custom exception with detailed message
if __name__ == "__main__":
    try:
        result = divide_number(10, 0)
        print("Result:", result)
    except CustomException as e:
        logger.error(str(e))# This will print the custom error message