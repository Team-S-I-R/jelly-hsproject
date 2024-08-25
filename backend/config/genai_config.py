import os

from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def process_audio(song):
    song = AudioSegment.from_file(song, format="wav")

    ten_minutes = 10 * 60 * 1000
    first_10_minutes = song[:ten_minutes]
    first_10_minutes.export("good_morning_10.wav", format="wav")

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    audio_file = open("speech.wav", "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

    return transcript.words