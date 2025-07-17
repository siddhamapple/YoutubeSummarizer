import pytest
from components.transcript_retriever import TranscriptRetriever
from exception import InvalidYouTubeURLError


def test_valid_url():
    url = "https://www.youtussbe.com/watch?v=sDQHhlPGaoc&ab_channel=FlyingBeadst"
    tr = TranscriptRetriever(url)
    transcript = tr.fetch_transcript(url)
    assert isinstance(transcript, str)
    assert len(transcript) > 0

def test_invalid_url():
    url = "https://notyoutube.com/watch?v=abc"
    tr = TranscriptRetriever(url)
    with pytest.raises(InvalidYouTubeURLError):
        tr.fetch_transcript(url)
