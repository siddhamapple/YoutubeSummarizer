import os
import sys
from logger import logging
from exception import CustomException
from dotenv import load_dotenv
from components.transcript_retriever import TranscriptRetriever
from components.preprocessor import Preprocessor
from components.qa_engine import QAEngine

def determine_chunk_size(transcript: str) -> int:
    length = len(transcript)
    if length < 2000:
        return length  # No chunking 
    elif length < 10000:
        return 3000
    elif length < 40000:
        return 8000
    else:
        return 12000  

def is_broad_question(question: str) -> bool:
    if not question.strip():
        return True
    broad_keywords = [
        "summary", "summarize", "main idea", "what is this video about", "overview",
        "overall", "topic", "objective", "agenda", "explain the video", "what happened",
        "components", "describe", "main points", "highlights", "structure", "key points"
    ]
    q_lower = question.lower()
    return any(kw in q_lower for kw in broad_keywords)

def main():
    try:
        url = input("Paste YouTube URL: ").strip()
        question = input("Enter your question (leave blank for summary): ").strip()

        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logging.error("GEMINI_API_KEY not found — set it in .env or environment.")
            print("[ERROR] GEMINI_API_KEY not found.")
            sys.exit(1)
        
        logging.info(f"Processing video at: {url}")

        # Step 1: Retrieve Transcript
        retriever = TranscriptRetriever(url)
        try:
            raw_transcript = retriever.fetch_transcript(url)
            logging.info(f"Transcript successfully retrieved. Length: {len(raw_transcript)} characters.")
        except Exception as e:
            logging.error(f"Could not retrieve transcript: {e}")
            print(f"[ERROR] Could not retrieve transcript: {e}")
            sys.exit(1)

        # Step 2: Preprocess (clean & chunk)
        preprocessor = Preprocessor()
        try:
            cleaned_transcript = preprocessor.clean_transcript(raw_transcript)
            chunk_size = determine_chunk_size(cleaned_transcript)
            logging.info(f"Dynamic chunk size determined: {chunk_size}")
            chunks = preprocessor.chunk_transcript(cleaned_transcript, chunk_size=chunk_size)
            logging.info(f"Transcript split into {len(chunks)} chunk(s).")
        except Exception as e:
            logging.error(f"Preprocessing failed: {e}")
            print(f"[ERROR] Preprocessing failed: {e}")
            sys.exit(1)
        
        engine = QAEngine(api_key=api_key)

        if is_broad_question(question):
            try:
                logging.info("Triggering map-reduce summarization for broad question.")
                chunk_answers = []
                prompt_for_chunk = question.strip() or "Give a concise summary of this transcript section."
                for idx, chunk in enumerate(chunks, 1):
                    print(f"\n--- Processing chunk {idx}/{len(chunks)} ---")
                    ans = engine.answer_question(chunk, prompt_for_chunk)
                    chunk_answers.append(ans)
                # Map step complete; reduce for single answer
                combined_answers = "\n\n".join(chunk_answers)
                reduce_prompt = (
                    f"Given these answers or explanations to the question '{question.strip() or 'Summarize the video'}' "
                    f"about a video's transcript, combine all information into a single, clear, non-redundant answer. "
                    f"Highlight all main points, remove repetitions, and provide a comprehensive response as if answering a user in one go.\n\n"
                    f"{combined_answers}"
                )
                summary = engine.summarize_transcript(reduce_prompt)
                print("\n=== UNIFIED FINAL ANSWER ===\n")
                print(summary)
            except Exception as e:
                logging.error(f"Unified summarization failed: {e}")
                print(f"[ERROR] Unified summarization failed: {e}")
        else:
            answers = []
            logging.info("Triggering per-chunk Q&A mode.")
            for idx, chunk in enumerate(chunks, 1):
                try:
                    print(f"\n--- Processing chunk {idx}/{len(chunks)} ---")
                    ans = engine.answer_question(chunk, question)
                    answers.append(ans)
                except Exception as e:
                    logging.warning(f"Q&A failed for chunk {idx}: {e}")
                    answers.append(f"[ERROR] Chunk {idx} failed: {e}")
            print("\n=== RELEVANT ANSWERS ===\n")
            for idx, ans in enumerate(answers, 1):
                print(f"Chunk {idx}: {ans}")

        logging.info("Pipeline execution completed.")
        
    except KeyboardInterrupt:
        print("\n[INFO] Exiting on user request.")
        logging.info("Execution interrupted by user.")
    except Exception as e:
        logging.error(f"Pipeline crashed: {e}", exc_info=True)
        print(f"\n[CRITICAL ERROR] {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
