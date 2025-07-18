#  YouTube Transcript Q&A & Summarizer

> AI-powered app that lets users **summarize** or **ask questions** about any YouTube video by processing its transcript through advanced **Large Language Models (LLMs)**.

---

##  Overview

YouTube Transcript Q&A & Summarizer is a modular, end-to-end pipeline that:
- Retrieves transcripts from YouTube videos
- Dynamically chunks long content for LLM processing
- Supports both **natural language Q&A** and **video summarization**
- Offers a **Streamlit web interface** for ease of use

This project transforms videos into searchable, interactive knowledge sources.

---

##  Features

-  **Instant Transcript Retrieval**  
  Extracts subtitles automatically from YouTube videos with available captions.

-  **LLM-Powered Summarization**  
  Converts long video transcripts into short, informative summaries.

-  **Ask Any Question**  
  Enter a natural language query and get an answer based on the video content.

-  **Map-Reduce Aggregation**  
  Efficiently processes long videos by chunking and combining answers or summaries.

-  **Streamlit Web App**  
  Simple, interactive user interface to upload links, ask questions, and view results.

-  **Downloadable Results**  
  Export generated summaries or answers as `.txt` files.

-  **Robust Testing**  
  Unit-tested modular pipeline using `pytest`.

-  **Logging & Error Handling**  
  Centralized logs and graceful failure mechanisms.

---

##  Project Structure

<img width="371" height="538" alt="image" src="https://github.com/user-attachments/assets/ed7a7270-5e3b-482a-ba3b-78beafce2318" />
<img width="393" height="689" alt="image" src="https://github.com/user-attachments/assets/776cc461-b820-43ec-8d93-1def499eab2f" />
<img width="366" height="784" alt="image" src="https://github.com/user-attachments/assets/81a9620d-abca-4037-b495-20e814673861" />

project-root/
├── app.py # Streamlit frontend
├── yt_logo.png # Logo for branding
├── requirements.txt # Dependencies
├── requirements-dev.txt # Dev dependencies (e.g. pytest)
├── pytest.ini # Pytest configuration
├── .env # API key and configs (not committed)
├── .gitignore # Git ignore rules
├── README.md # Project documentation
├── setup.py # For packaging (optional)
├── logs/ # Runtime logs
├── src/
│ ├── init.py
│ ├── components/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── preprocessor.py
│ │ ├── qa_engine.py
│ │ ├── transcript_retriever.py
│ │ └── internalTesting/ # Optional submodules
│ ├── logger.py # Centralized logging
│ ├── exception.py # Error handler
│ └── utils.py # Helper utilities
└── tests/
├── test_preprocessor.py
├── test_qa_engine.py
└── test_transcript_retriever.py



###  Prerequisites

- Python 3.8+
- YouTube video with captions
- Gemini API key (or any supported LLM)

---

###  Installation

```
git clone https://github.com/siddhamapple/YoutubeSummarizer
cd YoutubeSummarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
or
pip install -r requirments-dev.txt if developer
```

### env
Create a .env file at the project root and paste your API

GEMINI_API_KEY=your_gemini_api_key_here

### USAGE
enter on cmd-> streamlit run app.py
Visit: http://localhost:8501


###  App Flow
`Paste YouTube Link

`Choose Mode: Summarize or Ask a Question

`Process Transcript

`LLM runs per chunk (Map-Reduce)

`Final answer/summary shown

`Optional: Download output as .txt


##  Running Tests
Run all tests using:

```bash
pytest
```
The testing suite covers the following modules:

✅ TranscriptRetriever: Verifies transcript fetch accuracy from YouTube

✅ Preprocessor: Validates chunking, cleaning, and formatting logic

✅ QnAEngine: Checks consistency and quality of LLM-generated answers/summaries

/tests/
├── test_preprocessor.py
├── test_qa_engine.py
└── test_transcript_retriever.py

Use ``requirements-dev.txt`` to install testing dependencies.

##  Core Technologies Used
| Tool/Library          | Description                                          |
| --------------------- | ---------------------------------------------------- |
| **Streamlit**         | Frontend UI for interacting with the app             |
| **Google Gemini API** | Large Language Model used for Q\&A and summarization |
| **python-dotenv**     | Manages `.env` configurations securely               |
| **Pytest**            | Testing framework for verifying backend logic        |
| **Custom Modules**    | Modular Python files built under `src/components/`   |


## Modular Design Components:

transcript_retriever.py: Fetches captions from YouTube

preprocessor.py: Cleans and chunks transcript

qa_engine.py: Interfaces with the LLM for Q&A/summaries



## Roadmap
Here’s what’s coming next:

 Multilingual Support: Auto-detect video language and translate

 Asynchronous Chunk Processing: Faster summarization with async LLM calls

 Deployment Options: Push to Streamlit Cloud / Hugging Face Spaces

 CLI Utilities: Command-line support for batch summarization

 UI Polish: Improve layout, theme, and mobile responsiveness



## 👨‍💻 Author
- Siddham Jain
- +919625208689
   Shiv Nadar IOE | B.Tech in Electrical and Computer Engineering
   siddhamjainn@gmail.com


##  Contributing
We welcome contributions! Follow these steps:

Fork this repository

Create a new feature branch (git checkout -b feature-name)

Commit your changes (git commit -am 'Add feature')

Push to the branch (git push origin feature-name)

Open a pull request 🚀
