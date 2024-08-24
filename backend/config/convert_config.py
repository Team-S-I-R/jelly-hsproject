from config.log import logger as log
from dataclasses import dataclass
import os
import sys
import time
import subprocess

@dataclass
class ExtensionTypes:
    WAV = "wav"
    MKV = "mkv"
    MP3 = "mp3"
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    FLAC = "flac"


BASE_PATH = "./uploads/"

def is_valid_extension(file: str) -> bool:
    if file not in ExtensionTypes.__annotations__.values():
        log.error(f"Invalid file extension provided for {file}.")
        return False

    return True


def is_valid(file: str, output: str) -> bool:
    if file is None or file == "":
        log.error("No sufficient file format, or file provided.")
        return True

    if output is None or output == "":
        log.error("No sufficient output format provided.")
        return True

    return False


# this converts mp4 to wav
def convert_mp4_to_wav(path):
    files = os.listdir(path)
    wav_files = []

    for file in files:
        log.info(f"Processing {file} in {path}")
        subprocess.run([
            "ffmpeg",
            "-i",
            f"{path}{file}",
            f"{path}{file.split('.')[0]}.wav"
        ])
        wav_files.append(f"{path}{file.split('.')[0]}.wav")
        log.info(f"Converted {file} to {file.split('.')[0]}.wav")
    
    return wav_files
# TODO: Read https://stackoverflow.com/questions/49669298/conversing-mp4-to-wav-with-the-same-file-name-in-python

