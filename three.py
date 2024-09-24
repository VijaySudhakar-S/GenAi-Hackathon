from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

# Function to extract video ID from a YouTube URL
def extract_video_id(url):
    video_id = re.search(r"(?<=v=)[^&]+", url)
    if video_id:
        return video_id.group(0)
    raise ValueError("Invalid YouTube URL")

# Function to get video transcript from YouTube
def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([item['text'] for item in transcript])
    return transcript_text

# Function to summarize the transcript using Hugging Face summarization model
def summarize_text(text):
    summarizer = pipeline("summarization")
    # Split text if it's too long for the model
    chunk_size = 1000  # Adjust as needed to avoid length issues
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    return " ".join(summaries)

# Example usage
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with the YouTube video URL
video_id = extract_video_id(video_url)  # Extract video ID from the URL
transcript = get_transcript(video_id)
summary = summarize_text(transcript)
print("Transcript Summary:")
print(summary)
