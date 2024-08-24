from flask import Flask, jsonify, request
from config.log import logger as log
from flask import abort, redirect, request
from deepface import DeepFace
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import requests
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sys
import time
import subprocess
from openai import OpenAI, OpenAIError

load_dotenv()

app = Flask(__name__)
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

IN_PATH = "./osin/"
OUT_PATH = "./osout/"
FFMPEG_PATH = os.getenv("FFMPEG_PATH")


# error handlers -----------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    response = {
        "error": "404: NOT FOUND.",
        "message": "THe requested resource you are looking for could not be found.",
        "status": 404
    }

    return jsonify(response), 404


@app.errorhandler(429)
def too_many_requests(error):
    response = {
        "error": "429: TOO MANY REQUESTS.",
        "message": "You have exceeded the maximum number of requests allowed.",
        "status": 429
    }

    return jsonify(response), 429


@app.errorhandler(500)
def internal_server_error(error):
    response = {
        "error": "500: INTERNAL SERVER ERROR.",
        "message": "Its not you, its us. We are experiencing some technical difficulties.",
        "status": 500
    }

    return jsonify(response), 500


# routes --------------------------------------------------------------------------

@app.route("/transcribe", methods=['POST'])
def transcribe():  # put application's code here
    if "file" not in request.files:
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No file part in the request.",
            "status": 400
        }), 400

    file = request.files["file"]

    file_path = f"./temp/{file.filename}"

    # turn .mp4 to .wav
    convert_mp4_to_wav(file_path) 

    file.save(file_path)

    # TODO: Turn .mp4 to .wav
    # TODO: Transcribe .wav file to text using AI (TBD)
    # TODO: Return transcribed text in JSON
    # TODO: Store in Database (TBD)
    # TODO: Delete .wav file ./uploads
    # TODO: Delete .mp4 file from ./temp

def convert_to_wav():
    try:

        api_key = os.getenv("OPENAI_API_KEY")

        openai = OpenAI(
            api_key=api_key,
            # project=os.getenv("OPENAI_PROJECT_ID"),
        )

    except OpenAIError as e:
        print(f"An error occurred while connecting to OpenAI: {e}")
        sys.exit(1)

def convert_mp4_to_wav(path):
    files = os.listdir(path)

    for file in files:
        print(f"Processing {file} in {path}")
        subprocess.run([
            "ffmpeg",
            "-i",
            f"{path}{file}",
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




# create_video -------------------------------------------------------------------

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(f"./uploads/{file.filename}_{time.time()}.")
def mapping(text):
    sentiment_scores = sid.polarity_scores(text)
    compound = sentiment_scores['compound']

    if compound >= 0.05:
        return {"Happy": compound}
    elif compound <= -0.05:
        return {"Sad": abs(compound)}
    else:
        return {"Neutral": 1 - abs(compound)}
def text_emotion_analysis(text):
    return mapping(text)

def face_emotion_analysis(file_path):
    result = DeepFace.analyze(img_path=file_path, actions=["emotion"])
    return result[0]["dominant_emotion"]


@app.route("/create-video", methods=['POST'])
def create_video():
    data = request.json
    transcript = data.get("transcript")
    audio_file = data.get("audio_file")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    response = genai.GenerativeModel(model_name="gemini-1.5-flash").generate_content([transcript])
    summary_text = response.text
    words = summary_text.split()
    chunk = 10
    chunks = [' '.join(words[i:i +chunk]) for i in range(0, len(words), chunk_size)]

    clips = []
    audio = AudioFileClip(audio_file)
    for chunk in chunks:
        pexels_api_key = os.getenv("PEXELS_API_KEY")
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": pexels_api_key},
            params={"query": chunk, "per_page": 1}
        )
        if response.status_code == 200:
            image_url =response.json()["photos"][0]["src"]["original"]
            image_clip = ImageClip(image_url).set_duration(15)
            clips.append(image_clip.set_audio(audio))

    final = CompositeVideoClip(clips)
    output = f"./uploads/video_{int(time.time())}.mp4"
    final.write_videofile(output, codec='libx264', audio_codec='aac')

    return jsonify({"message": "video created!", "video_url": output_file}), 200

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    start_time = time.time()
    app.run(debug=True)
    log.info(f"Application started in {time.time() - start_time} seconds")
