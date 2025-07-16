Simple file for now->
-main.py: The main application—wires everything together and handles running the app (and possibly the UI).

-transcript_retriever.py: Handles retrieving transcripts from YouTube URLs.

-preprocessor.py: Cleans and processes transcript text for the LLM.

-qa_engine.py: Contains logic to interact with your LLM and answer questions.

-exceptions.py: Custom exceptions for handling known error situations in a clean way.

-logger.py: Sets up a structured, reusable logging facility.

-tests/: Contains test scripts for each main module.

-Other files: README.md, requirements.txt, setup.py, etc., are for documentation and configuration.