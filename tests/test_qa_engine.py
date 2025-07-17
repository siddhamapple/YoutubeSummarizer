import pytest
from unittest.mock import patch, MagicMock
from components.qa_engine import QAEngine
from exception import LLM_APIError,CustomException
@patch('google.generativeai.GenerativeModel.generate_content')
def test_answer_question_success(mock_generate):
    mock_response = MagicMock()
    mock_response.text = "QA Answer"
    mock_generate.return_value = mock_response

    qa = QAEngine(api_key="dummy")
    result = qa.answer_question("chunk", "question")
    assert result == "QA Answer"

@patch('google.generativeai.GenerativeModel.generate_content')
def test_answer_question_retry(mock_generate):
    mock_generate.side_effect = [Exception("fail"), MagicMock(text="QA Answer")]
    qa = QAEngine(api_key="dummy", max_retries=2, base_delay=0)
    result = qa.answer_question("chunk", "question")
    assert result == "QA Answer"

@patch('google.generativeai.GenerativeModel.generate_content')
def test_answer_question_fail_all(mock_generate):
    mock_generate.side_effect = Exception("Fail")
    qa = QAEngine(api_key="dummy", max_retries=1, base_delay=0)
    result = qa.answer_question("chunk", "question")
    assert result.startswith("My bad")
