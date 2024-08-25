import os
import time
import requests

from flask import Flask, jsonify, request
# do not change this
from flask_cors import CORS
from config.log import logger as log
from dotenv import load_dotenv

import nltk
from deepface import DeepFace
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
from config.error_config import register_error_handlers
from config.convert_config import convert_mp4_to_wav
from handler.error_handler import handle_200_json, handle_400_json, handle_404_json, handle_429_json
from werkzeug.utils import secure_filename
from config.genai_config import process_audio
from config.captions_config import add_captions
from config.upload_config import upload_file_to_supabase
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
        "http://localhost:3000", 
    "http://localhost:3001", 
    "http://localhost:3002", 
])
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

register_error_handlers(app)

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {
    "mp4",
    "mp3",
    "wav",
    "avi"
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/main", methods=['POST'])
def transcribe():
    """
    Transcribe the audio file to text (transcribe) with timestamps.

    :return: JSON response.
    """

    if "file" not in request.files:
        return handle_400_json(message="400: BAD REQUEST. NO FILE PART.")

    file = request.files["file"]
    
    if file.filename == '':
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No selected file.",
            "status": 400,
            "date": time.time()
        }), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        log.info(f"File saved at: {file_path}")

        input_path = file_path
        print(f"Input_Path: {input_path}")
        output_path = './temp/captioned_Video.mp4'
        
        convertedWav = convert_mp4_to_wav(input_path)
        
        # # TODO: Transcribe .wav file to text using AI (config/transcribe_config.py)
        # # TODO: Return transcribed text in JSON
        time.sleep(2)
        captions_path = process_audio(convertedWav)

        # TODO: Turn captions into s .srt file (captions file)
        add_ct = add_captions(input_path, output_path, captions_path)
        
        # TODO: Store in Database (TBD)
        upload = upload_file_to_supabase(add_ct, filename)
        time.sleep(1)
        
        # TODO: Delete files
        new_filename = filename.replace('.mp4', '.wav')
        os.remove(f'./temp/{filename}')
        time.sleep(1)
        os.remove(f'./temp/{new_filename}')    
        time.sleep(1)
        os.remove('./temp/captioned_Video.mp4')
        time.sleep(1)

        return jsonify({
            "message": "File successfully uploaded and processed.",
            "url": upload,
            "status": 200,
            "date": time.time()
        }), 200
        # return handle_200_json(message="200: SUCCESSFULLY TRANSCRIBED.")

    return handle_400_json(message="400: BAD REQUEST. FILE TYPE NOT ALLOWED.")


# TODO: COMPLETE FUNCTION!
@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload a file to the server (./uploads folder).

    :return: JSON response.
    """

    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(f"./uploads/{file.filename}_{time.time()}.")


def mapping(text):
    """
    Map the sentiment analysis to a dictionary.

    :param text: the text to analyze for sentiment.
    :return: A dictionary with the sentiment analysis.
    """

    sentiment_scores = sid.polarity_scores(text)
    compound = sentiment_scores['compound']

    if compound >= 0.05:
        return {"Happy": compound}

    elif compound <= -0.05:
        return {"Sad": abs(compound)}

    else:
        return {"Neutral": 1 - abs(compound)}


def text_emotion_analysis(text):
    """
    Analyze the emotion of the text.
    :param text: The text to analyze for sentiment.
    :return: The emotion of the text.
    """

    return mapping(text)


def face_emotion_analysis(file_path):
    """
    Analyze the emotion of the face in the video/image.

    :param file_path: The path to the video/image file.
    :return: The emotion of the face in the video/image.
    """

    result = DeepFace.analyze(img_path=file_path, actions=["emotion"])
    return result[0]["dominant_emotion"]


@app.route("/create-video", methods=['POST'])
def create_video():
    """
    Create a video from the transcript and audio file.

    :return: JSON response.
    """

    data = request.json
    transcript = data.get("transcript")
    audio_file = data.get("audio_file")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    response = genai.GenerativeModel(model_name="gemini-1.5-flash").generate_content([transcript])
    summary_text = response.text
    words = summary_text.split()
    chunk = 10
    chunks = [' '.join(words[i:i + chunk]) for i in range(0, len(words), chunk)]

    clips = []
    audio = AudioFileClip(audio_file)
    for chunk in chunks:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={
                "Authorization": os.getenv("PEXELS_API_KEY")
            },
            params={
                "query": chunk,
                "per_page": 1
            }
        )
        if response.status_code == 200:
            image_url = response.json()["photos"][0]["src"]["original"]
            image_clip = ImageClip(image_url).set_duration(15)
            clips.append(image_clip.set_audio(audio))

    final = CompositeVideoClip(clips)
    output = f"./uploads/video_{int(time.time())}.mp4"
    final.write_videofile(output, codec='libx264', audio_codec='aac')

    return jsonify({
        "message": "200: SUCCESSFULLY CREATED VIDEO.",
        "status": 200,
        "date": time.time(),
        "output": output
    }), 200


if __name__ == '__main__':
    start_time = time.time()
    app.run(debug=True)
    log.info(f"Application started in {time.time() - start_time} seconds")
