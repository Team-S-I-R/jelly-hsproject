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


def is_valid_extension(file: str) -> bool:
    """
    Check if the file has a valid file extension for conversion.

    :param file: The file to check.
    :return: True if the file has a valid extension, otherwise False.
    """

    for ext in ExtensionTypes.__annotations__.values():
        if ext in file:
            return True

    return False


def is_valid(file: str, output: str) -> bool:
    if file is None or file == "":
        log.error("No sufficient file format, or file provided.")
        return True

    if output is None or output == "":
        log.error("No sufficient output format provided.")
        return True

    return False


# this converts mp4 to wav
def convert_mp4_to_wav(file_path: str) -> str | None:
    """
    Convert an .mp4 file to .wav format.

    :param file_path: The path to the .mp4 file.
    :return: The path to the converted .wav file.
    """
    
    is_valid_extension(file_path)

    try:
        normalized_path = os.path.normpath(file_path)  # Normalized path
        
        # ./temp and the xxx.mp4
        directory, filename = os.path.split(normalized_path)

        # xxx.mp4
        filename_without_ext = os.path.splitext(filename)[0]

        # building new path for wav 
        output_wav = os.path.join(directory, f"{filename_without_ext}.wav")
        log.info(f"Processing {normalized_path} in {directory}")

        subprocess.run([
            "ffmpeg",
            "-y",
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
