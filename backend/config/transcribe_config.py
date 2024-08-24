from ffmpy import FFmpeg, FFRuntimeError
from config.log import logger as log
from dataclasses import dataclass

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


def extract_audio_format_wav(file: str, output: str, extension: str) -> None:
    out_file = f"{BASE_PATH}{output}.{extension}"

    try:
        ff = FFmpeg(
            inputs={file: None},
            outputs={out_file: None},
            global_options=["-y"],
        )

    except FFRuntimeError as e:
        log.error(f"Error extracting audio from {file} to {output}.{extension}: {e}")

    else:
        log.info(f"Extracting audio from {file} to {output}.{extension}")
        ff.run()


# TODO: Read https://stackoverflow.com/questions/49669298/conversing-mp4-to-wav-with-the-same-file-name-in-python

