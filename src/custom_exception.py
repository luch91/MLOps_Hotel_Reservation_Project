import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: Exception) -> None:
        """
        Custom Exception class that provides detailed error message with traceback info.
        """
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: Exception) -> str:
        """
        Returns a detailed error message with the file name, line number, and error message.
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            stack_trace = traceback.format_exc()
            return (f"Error occurred in script: [{file_name}] at line number: [{line_number}] "
                    f"with error message: [{error_message}]\nStack Trace:\n{stack_trace}")
        else:
            return f"Error occurred: {error_message} (no traceback available)"

    def __str__(self) -> str:
        return self.error_message