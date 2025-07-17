import time
import google.generativeai as genai  
import os
#from google import genai
from exception import CustomException,LLM_APIError 
from logger import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GEMINI_API_KEY')


class QAEngine:
    """
    QAEngine integrates with an LLM API to provide Q&A and summarization over transcript chunks,
    with robust logging and exponential backoff for error resilience.
    """
    def __init__(self, api_key, max_retries=3, base_delay=2):
        self.max_retries = max_retries
        self.base_delay = base_delay
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            logging.error(f"Failed to initialize Gemini model: {e}")
            raise CustomException(f"Model initialization failed: {e}")




    def _call_llm_api(self, prompt):
        # Helper to call Gemini and return text, raise for API errors
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text
            return response.candidates[0]['content']['parts'][0]['text']  # fallback for other model, dig into the nested structure of the raw API response object:
        except Exception as e:
            logging.error(f"Gemini API Exception: {e}")
            raise LLM_APIError





    def answer_question(self, transcript_chunk, question):
        """
        Answer a user question using a transcript chunk & QA prompt.
        Handles retries, logs inputs/outputs/errors, returns answer string or fallback.
        """
        prompt = f"""Given this transcript chunk from a YouTube video: {transcript_chunk} ,Answer this question as thoroughly and accurately as possible :{question}"""
        logging.info(f"Attempting QA for question: '{question[:60]}...' | Chunk length: {len(transcript_chunk)}")
        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = time.perf_counter()
                answer = self._call_llm_api(prompt)
                duration = time.perf_counter() - start_time
                logging.info(f"QA success (attempt {attempt}) | Time: {duration:.2f}s | Answer length: {len(answer)}")
                return answer.strip()
            except Exception as e:
                wait = self.base_delay * (2 ** (attempt - 1))
                logging.warning(f"QA attempt {attempt} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
        logging.error("QAEngine: Max retries exceeded for QA. Returning fallback answer.")
        return "My bad, I cant process your request at this time, try again."






    def summarize_transcript(self, transcript_or_chunks):
        """
        Summarize an entire transcript or list of chunks.
        Handles retries, logs steps, returns summary string or fallback.
        """
        if isinstance(transcript_or_chunks, list): 
            input_text = " ".join(transcript_or_chunks)
        else:
            input_text = transcript_or_chunks
        prompt = f"""Summarize the following YouTube transcript. Keep it concise, covering main topics, speakers, and key facts.Transcript: {input_text}  """
        logging.info(f"Attempting summarization | Input length: {len(input_text)}")
        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = time.perf_counter()
                summary = self._call_llm_api(prompt)
                duration = time.perf_counter() - start_time
                logging.info(f"Summarization success (attempt {attempt}) | Time: {duration:.2f}s | Summary length: {len(summary)}")
                return summary.strip()
            except Exception as e:
                wait = self.base_delay * (2 ** (attempt - 1))
                logging.warning(f"Summarization attempt {attempt} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
        logging.error("QAEngine: Max retries exceeded for summarization. Returning fallback summary.")
        return "Summary unavailable due to system error."
