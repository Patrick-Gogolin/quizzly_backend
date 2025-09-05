import yt_dlp
import whisper
from google import genai
import os
from dotenv import load_dotenv
import tempfile

QUIZZ_PROMPT_TEMPLATE = """
Based on the following transcript, generate a quiz in valid JSON format.

Return only valid JSON, no markdown, no backticks, no explanations.

The quiz must follow this exact structure:

{
"title": "Create a concise quiz title based on the topic of the transcript.",
"description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
"questions": [
    {
    "question_title": "The question goes here.",
    "question_options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The correct answer from the above options"
    },
    ... (exactly 10 questions)
]
}

Requirements:
- Each question must have exactly 4 distinct answer options.
- Only one correct answer is allowed per question, and it must be present in 'question_options'.
- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
- Do not include explanations, comments, or any text outside the JSON.

Here is the transcript:
"""

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def download_audio(url: str) -> str:
        tmp_dir = tempfile.gettempdir()
        tmp_filename = os.path.join(tmp_dir, "audio.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": tmp_filename,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                audio_file = filename.rsplit(".", 1)[0] + ".wav"
                return audio_file

def transcribe_audio(audio_file: str) -> str:
        model = whisper.load_model("tiny")
        transcript = model.transcribe(audio_file)
        return transcript['text']

def generate_quiz(transcript: str) -> str:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"{QUIZZ_PROMPT_TEMPLATE}\n{transcript}\n"
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text