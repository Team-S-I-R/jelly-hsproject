# TODO: Complete Backend Subtitle Transcriber
import os
import sys
import time
import subprocess

from dotenv import load_dotenv
# from log import logger as log
from openai import OpenAI, OpenAIError

IN_PATH = "./osin/"
OUT_PATH = "./osout/"
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

# Load .env
load_dotenv(dotenv_path=".env")

# AI config
try:
    openai = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        project=os.getenv("OPENAI_PROJECT_ID"),
    )

except OpenAIError as e:
    print(f"An error occurred while connecting to OpenAI: {e}")
    sys.exit(1)

def convert_mp4_to_wav():
    files = os.listdir(IN_PATH)

    for file in files:
        print(f"Processing {file} in {IN_PATH}")
        subprocess.run([
            "ffmpeg",
            "-i",
            f"{IN_PATH}{file}",
            f"{OUT_PATH}{file.split('.')[0]}.wav"
        ])
        print(f"Converted {file} to {OUT_PATH}{file.split('.')[0]}.wav")


def transcribe_wav_to_text() -> str:
    if not os.listdir(OUT_PATH):
        print(f"No files found in the output {OUT_PATH} directory.")
        sys.exit(1)

    for file in os.listdir(OUT_PATH):
        print(f"Found file: {file}")

        if file.endswith(".wav"):
            print(f"Transcribing {file} using openai-whisper as verbose_json")
            file_path = os.path.join(OUT_PATH, file)

            try:
                with open(file_path, "rb") as audio_wav:
                    transcriber = openai.audio.transcriptions.create(
                        model=os.getenv("OPENAI_MODEL"),
                        file=audio_wav,
                        timeout=120,  # 2 minutes
                        response_format="verbose_json"  # verbose_json or srt (srt for subtitles)
                    )
                    print(transcriber.json())

            except FileNotFoundError as fnf_error:
                print(f"File not found: {fnf_error}")
                sys.exit(1)

            except OpenAIError as oai_error:
                print(f"An error occurred while transcribing (OpenAIError): {oai_error}")


if __name__ == "__main__":
    convert_mp4_to_wav()
    time.sleep(5)
    transcribe_wav_to_text()
