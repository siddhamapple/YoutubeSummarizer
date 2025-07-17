import pytest
from components.preprocessor import Preprocessor
from exception import CustomException

def test_clean_transcript_removes_noise():
    raw = "[Music] 00:01 Hello world! [Noise] 00:02 Bye."
    expected = "Hello world! Bye."
    pre = Preprocessor()
    out = pre.clean_transcript(raw)
    assert expected in out

def test_chunk_transcript_basic():
    text = "Sentence one. Sentence two. Sentence three. Sentence four."
    pre = Preprocessor()
    chunks = pre.chunk_transcript(text, chunk_size=20)
    assert all(len(chunk) <= 20 for chunk in chunks)
    assert "".join(chunks).replace(" ", "") in text.replace(" ", "")

def test_exception_on_invalid_input():
    pre = Preprocessor()
    with pytest.raises(CustomException):
        pre.clean_transcript(1234)
