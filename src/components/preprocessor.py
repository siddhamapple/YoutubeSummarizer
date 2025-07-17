import re
from logger import logging
from exception import CustomException

class Preprocessor:
    """
    Preprocessor class for cleaning and splitting YouTube transcripts.
    - Removes timestamps, bracketed annotations, and normalizes whitespace.
    - Can chunk long text into manageable pieces for LLMs.
    """

    def __init__(self, remove_patterns=None):
       
        self.remove_patterns = remove_patterns or [
            r"\[.*?\]",                 # [Music], [Applause], etc.
            r"\d{1,2}:\d{2}(?::\d{2})?",# 00:01 or 00:01:02 timestamps
        ]
    
    def clean_transcript(self, text):
        """
        Cleans transcript text.
        Removes timestamps, bracketed content, extra spaces.
        """
        try:
            if not isinstance(text, str):
                logging.error("Input to clean_transcript is not a string.")
                raise CustomException("Input must be a string for cleaning transcript.")
            
            original_length = len(text)
            logging.info(f"Starting transcript cleaning. Original length: {original_length} chars.")

            for pattern in self.remove_patterns:
                text = re.sub(pattern, "", text)
            text = ' '.join(text.split())

            cleaned_length = len(text)
            logging.info(f"Transcript cleaned. Cleaned length: {cleaned_length} chars. Chars removed: {original_length - cleaned_length}.")

            return text
        except Exception as e:
            logging.error(f"Exception during clean_transcript: {e}")
            raise CustomException(e)

    def chunk_transcript(self, text, chunk_size=1000):
        """
        Splits text into chunks of approximately chunk_size characters.
        """
        try:
            if not isinstance(text, str):
                logging.error("Input to chunk_transcript is not a string.")
                raise CustomException("Input must be a string for chunking transcript.")

            if chunk_size < 1:
                raise ValueError("Chunk size must be greater than zero.")
            if chunk_size < 200:
                logging.warning("Chunk size is very small; this may split text into many tiny pieces.")


            chunks = []
            start = 0
            text_length = len(text)

           
            while start < text_length:
                end = min(start + chunk_size, text_length)
                if end < text_length:
                    # Try to break at the nearest space for readability, not in the middle of words
                    space_pos = text.rfind(' ', start, end)
                    if space_pos != -1 and space_pos > start:
                        end = space_pos
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start = end

            logging.info(f"Transcript split into {len(chunks)} chunks with approx. {chunk_size} chars per chunk.")
            return chunks
        except Exception as e:
            logging.error(f"Exception during chunk_transcript: {e}")
            raise CustomException(e)
