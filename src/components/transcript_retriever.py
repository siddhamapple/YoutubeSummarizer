import re
from youtube_transcript_api import YouTubeTranscriptApi
from logger import logging
from exception import CustomException
from urllib.parse import urlparse, parse_qs
from exception import CustomException, TranscriptNotFoundError, InvalidYouTubeURLError
from youtube_transcript_api._errors import NoTranscriptFound, CouldNotRetrieveTranscript


class TranscriptRetriever():
    '''
    Class to fetch the transcript of the youtube video
    '''
    
    def __init__(self,youtube_url):
        self.youtube_url=youtube_url

    @staticmethod
    def is_valid_youtube_url(url):
        '''
        Checks if the URL is a valid YouTube link to prevent unnecesary API call
        '''
        logging.info(f"Checking for valid URL->{url}")
        youtube_pattern = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+')
        return bool(youtube_pattern.match(url))
    
    def fetch_uid_yt(self, youtube_url):
     """
      Retrieves the UID (video ID) from a variety of YouTube URL formats.
     """
     parsed_url = urlparse(youtube_url)
     if "youtu.be" in parsed_url.netloc:
        # Short link format: youtu.be/VIDEO_ID
        uid = parsed_url.path.lstrip("/")
        logging.info(f"Fetched youtube url uid -> {uid}")
     elif "youtube.com" in parsed_url.netloc:
        if parsed_url.path == "/watch":
            # Standard format: yout     ube.com/watch?v=VIDEO_ID
            query_params = parse_qs(parsed_url.query)
            uid_list = query_params.get("v")
            if uid_list:
                uid = uid_list[0]
                logging.info(f"Fetched youtube url uid -> {uid}")
            else:
                raise InvalidYouTubeURLError("No video ID found in query parameters.")
        elif parsed_url.path.startswith("/shorts/"):
            # Shorts format: youtube.com/shorts/VIDEO_ID
            uid = parsed_url.path.split("/shorts/")[-1].split("/")[0]
            logging.info(f"Fetched youtube url uid -> {uid}")
        else:
            raise InvalidYouTubeURLError("URL does not match recognized YouTube formats.")
     else:
        raise InvalidYouTubeURLError("Not a recognized YouTube URL.")
     return uid


    def fetch_transcript(self, youtube_url):
        '''
        Retrieves and returns the transcript 
        '''
        if not self.is_valid_youtube_url(self.youtube_url):
            logging.error("Got invalid URL, Raising error Valid URL")
            raise InvalidYouTubeURLError("Not a valid YouTube URL")
        
        try:
            uid = self.fetch_uid_yt(youtube_url)
            logging.info(f"Fetched uid ->{uid} and Fetching transcription")
            
            # Get transcript directly using get_transcript
            transcript = YouTubeTranscriptApi.get_transcript(uid)
            # Join all text entries
            transcript_text = " ".join(entry.get('text', '') for entry in transcript)
            return transcript_text
        except (NoTranscriptFound, CouldNotRetrieveTranscript) as ce:
            logging.error(f"Transcript error: {ce}")
            raise TranscriptNotFoundError(ce)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise CustomException(e)