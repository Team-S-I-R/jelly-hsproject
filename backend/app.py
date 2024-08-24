from flask import Flask, jsonify, request
from config.log import logger as log
from flask import abort, redirect
from deepface import DeepFace
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import requests
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
import os
from dotenv import load_dotenv
import google.generativeai as genai
from config.error_config import register_error_handlers
from config.captions_config import add_captions
from config.convert_config import convert_mp4_to_wav
from config.genai_config import process_audio
from config.upload_config import upload_file_to_supabase
import cv2
from werkzeug.utils import secure_filename


load_dotenv()

app = Flask(__name__)
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# registering error handlers in error_config.py
register_error_handlers(app)

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/main", methods=['POST'])
def transcribe():  
    if "file" not in request.files:
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No file part in the request.",
            "status": 400
        }), 400

    file = request.files["file"]
    
    if file.filename == '':
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No selected file.",
            "status": 400
        }), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        log.info(f"File saved at: {file_path}")

        input_path = file_path
        print("input_path", input_path)
        
        convertedWav = convert_mp4_to_wav(input_path)
        # # TODO: Transcribe .wav file to text using AI (config/transcribe_config.py)
        # # TODO: Return transcribed text in JSON
        time.sleep(2)
        captions_text = process_audio(convertedWav)
        # # TODO: Add text to video (config/captions_config.py)

        # # TODO: Tunr captions into s .srt file (captions file)
        add_ct = add_captions(input_path, convertedWav, captions_text)
        # # TODO: Store in Database (TBD)
        # upload = upload_file_to_supabase(convertedWav)
        # # TODO: Return video url
        # print("Done!")
        # return add_ct
        # # TODO: Delete .wav file ./uploads
        # # TODO: Delete .mp4 file from ./temp
        
        # log.info(f"Temporary files removed: {wav_path} and {file_path}")
        
        # time.sleep(2)
        # print("removing temporary files...")
       
        # os.remove(wav_path)
        # os.remove(file_path)
        
        # if success
        return jsonify({
            "message": "Transcription completed successfully.",
            "status": 200
        }), 200

    # if bad request
    return jsonify({
        "error": "400: BAD REQUEST.",
        "message": "File type not allowed.",
        "status": 400
    }), 400


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
    chunks = [' '.join(words[i:i + chunk]) for i in range(0, len(words), chunk_size)]

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
            image_url = response.json()["photos"][0]["src"]["original"]
            image_clip = ImageClip(image_url).set_duration(15)
            clips.append(image_clip.set_audio(audio))

    final = CompositeVideoClip(clips)
    output = f"./uploads/video_{int(time.time())}.mp4"
    final.write_videofile(output, codec='libx264', audio_codec='aac')

    return jsonify({"message": "video created!"}), 200


if __name__ == '__main__':
    start_time = time.time()
    app.run(debug=True)
    log.info(f"Application started in {time.time() - start_time} seconds")
