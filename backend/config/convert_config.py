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
def convert_mp4_to_wav(file_path):
    try:
        # Normalize the file path
        normalized_path = os.path.normpath(file_path)
        
        # Get the directory and filename
        directory, filename = os.path.split(normalized_path)
        
        # Get the filename without extension
        filename_without_ext = os.path.splitext(filename)[0]
        
        # Create the output wav file path
        output_wav = os.path.join(directory, f"{filename_without_ext}.wav")
        
        log.info(f"Processing {normalized_path}")
        
        # Run ffmpeg command with the -y flag to overwrite if the file exists
        subprocess.run([
            "ffmpeg",
            "-y",  # Automatically overwrite output file if it exists
            "-i",
            normalized_path,
            output_wav
        ], check=True)
        
        log.info(f"Converted {filename} to {filename_without_ext}.wav")
        
        return output_wav
    
    except subprocess.CalledProcessError as e:
        log.error(f"Error during conversion: {e}")
        return None
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return None
