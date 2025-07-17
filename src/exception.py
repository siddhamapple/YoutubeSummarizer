import sys
import traceback

def error_message_detail(error):
    exc_type, exc_value, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
    line_no = exc_tb.tb_lineno if exc_tb else "Unknown"
    return f"Error occurred at [{file_name}] on line [{line_no}]: {error}"

class CustomException(Exception):
    """Base class for custom exceptions in this project."""
    def __init__(self, error):
        super().__init__(str(error))
        self.error_message = error_message_detail(error)
        
    def __str__(self):
        return self.error_message

class TranscriptNotFoundError(CustomException):
    """Raised when a transcript cannot be retrieved for a YouTube video."""
    pass

class InvalidYouTubeURLError(CustomException):
    """Raised when the provided YouTube URL is invalid or unsupported."""
    pass

class LLM_APIError(CustomException):
    """Raised when an error occurs with the LLM API call."""
    pass