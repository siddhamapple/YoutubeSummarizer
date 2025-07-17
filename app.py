import streamlit as st
import os
import sys
from logger import logging
from exception import CustomException
from dotenv import load_dotenv
import os
from components.transcript_retriever import TranscriptRetriever
from components.preprocessor import Preprocessor
from components.qa_engine import QAEngine


load_dotenv()

def get_summary(video_url, question):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment or .env file.")

    # Step 1: Retrieve transcript
    retriever = TranscriptRetriever(video_url)
    raw_transcript = retriever.fetch_transcript(video_url)

    
    preprocessor = Preprocessor()
    cleaned = preprocessor.clean_transcript(raw_transcript)

    def determine_chunk_size(transcript):
        length = len(transcript)
        if length < 2000:
            return length
        elif length < 10000:
            return 3000
        elif length < 40000:
            return 8000
        else:
            return 12000

    chunk_size = determine_chunk_size(cleaned)
    chunks = preprocessor.chunk_transcript(cleaned, chunk_size=chunk_size)

    engine = QAEngine(api_key=api_key)

    # Determine mode: summarize if question is blank or summarization requested
    if (not question) or "summary" in question.lower() or "summarize" in question.lower():
        # Map-reduce summarization
        summaries = [engine.answer_question(chunk, "Summarize this transcript section.") for chunk in chunks]
        combined = "\n\n".join(summaries)
        reduce_prompt = (
            f"Given these summaries/explanations from different parts of the video, "
            f"write a single, clear summary covering all key points:\n\n{combined}"
        )
        final_summary = engine.summarize_transcript(reduce_prompt)
        return final_summary
    else:
        # Per-chunk Q&A
        answers = [engine.answer_question(chunk, question) for chunk in chunks]
        return "\n\n".join([f"Chunk {i+1}:\n{ans}" for i, ans in enumerate(answers)])


st.set_page_config(page_title="YouTube Transcript Q&A & Summarizer")


ICON_PATH = "yt_logo.png"
st.image(ICON_PATH, width=100)

st.title(" YouTube Transcript Q&A & Summarizer")
st.markdown("Enter YouTube video link and choose an action:")

video_url = st.text_input("YouTube Video Link", placeholder="Paste the URL here...")

option = st.radio("Select Action:", ("Summarize Video", "Ask a Question"))

question = ""
if option == "Ask a Question":
    question = st.text_input("Enter your question about this video:")

if st.button("Go") and video_url:
    with st.spinner("Processing..."):
        try:
            output_text = get_summary(video_url, question)
        except Exception as e:
            output_text = f"Error: {str(e)}"

        st.subheader("Output:")
        st.write(output_text)

        st.download_button(
            label="Download Output",
            data=output_text,
            file_name="output.txt",
            mime="text/plain"
        )

st.markdown("Created by **Siddham Jain** (Student of Shiv Nadar IOE).")
