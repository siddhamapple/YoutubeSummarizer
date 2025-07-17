from components.transcript_retriever import TranscriptRetriever

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=sDQHhlPGaoc&t=1s&ab_channel=FlyingBeast"  # Replace with any valid YouTube URL
    retriever = TranscriptRetriever(url)
    try:
        transcript = retriever.fetch_transcript(url)
        print("Sample transcript excerpt:")
        print(transcript[:600])  # Show the beginning for sanity check
    except Exception as e:
        print(f"Error: {e}")
