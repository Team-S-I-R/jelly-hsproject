import os
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
from config.log import logger as log

load_dotenv(dotenv_path=".env")


def process_audio(song):
    song = AudioSegment.from_file(song, format="wav")

    ten_minutes = 10 * 60 * 1000
    first_10_minutes = song[:ten_minutes]
    temp_wav_path = "processed_10_minutes.wav"
    first_10_minutes.export(temp_wav_path, format="wav")
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    with open(temp_wav_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
    )
    
    log.info(f"Transcript: {transcript}")
    return transcript.words