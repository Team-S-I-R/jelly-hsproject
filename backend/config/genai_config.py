import os

from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL = "gpt-4o"

ak = os.getenv("OPENAI_API_KEY")
# AI Config
client = OpenAI(
    api_key=ak,
)


def query_chatgpt(user_content: str, system_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Here are the words and timestamps: {user_content}",
            }
        ],
        temperature=0.9,
        frequency_penalty=0
    )

    response_text = response.choices[0].message.content.strip()

    # Ensure the temp directory exists
    os.makedirs('./temp', exist_ok=True)

    # Define the file path
    file_path = './temp/response.srt'

    # Write the response text to the file
    with open(file_path, 'w') as file:
        file.write(response_text)

    return file_path


def process_audio(file_path):
    # Convert the input file to WAV format if it's not already
    if not file_path.lower().endswith('.wav'):
        audio = AudioSegment.from_file(file_path)
        wav_path = './temp/converted_audio.wav'
        audio.export(wav_path, format='wav')
    else:
        wav_path = file_path

    with open(wav_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )

    system = (
        "You are a subtitle generator. I will provide you with a transcript of a video, and I need you to format it "
        "into SubRip Subtitle (.srt) file format."
        "DO NOT include formatting or code blocks!!!!!!!!!! Just give me the transcript in the format we am asking for"
        "The .srt format consists of subtitles with the following structure:\n\n"
        "1\n"
        "00:00:01,000 --> 00:00:05,000\n"
        "This is the first subtitle.\n\n"
        "2\n"
        "00:00:05,000 --> 00:00:10,000\n"
        "This is the second subtitle.\n\n"
        "Please use appropriate timestamps and split the transcript into subtitles based on natural breaks. "
        "Also, please account for the pauses that the speaker(s) may have when generating the timestamps. Do not just make them come one after another intelligently make the appropriate pauses.\n\n"
        "Here is the transcript text:\n\n"
    )

    words = transcript.words

    srtfile = query_chatgpt(words, system)

    return srtfile
