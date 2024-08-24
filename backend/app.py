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
import cv2

load_dotenv()

app = Flask(__name__)
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# registering error handlers in error_config.py
register_error_handlers(app)



# step 1: parse the srt file. we need to get the text and the times
def parse_srt(srt_path):
    """Parse the SRT file into a list of tuples with start time, end time, and caption text."""
    captions = []
    with open(srt_path, 'r') as file:
        srt_content = file.read()
        
        # Split SRT file into blocks of subtitle entries
        blocks = srt_content.strip().split('\n\n')
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                # Extract time range and text
                time_range = lines[1]
                start_time, end_time = time_range.split(' --> ')
                caption_text = ' '.join(lines[2:])
                
                captions.append({
                    'start_time': convert_srt_time_to_seconds(start_time),
                    'end_time': convert_srt_time_to_seconds(end_time),
                    'text': caption_text
                })
                
    return captions

# step 2: convert the srt time format to seconds
def convert_srt_time_to_seconds(srt_time):
    """Convert SRT time format (HH:MM:SS,MMM) to seconds."""
    h, m, s, ms = map(int, re.split('[:,]', srt_time))
    return int(h) * 3600 + int(m) * 60 + int(s) + int(srt_time.split(',')[1]) / 1000

# step 3: wrap text to fit within a given width. this prevents text from overflowing
def wrap_text(text, font, font_scale, font_thickness, max_width):
    """Wrap text to fit within a given width."""
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = f'{current_line} {word}'.strip()
        text_size, _ = cv2.getTextSize(test_line, font, font_scale, font_thickness)
        text_width = text_size[0]
        
        if text_width > max_width:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
        else:
            current_line = test_line
            
    if current_line:
        lines.append(current_line)
        
    return lines

# step 4: apply a filter to a video frame if there are any
def add_filters(frame, filter_type='grayscale'):
    """Apply a filter to a video frame."""
    if filter_type == 'grayscale':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'blur':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_type == 'edge_detection':
        return cv2.Canny(frame, 100, 200)
    else:
        return frame  # No filter applied

# step 5: add the captions to each frame
def add_captions(input_path, output_path, captions_path, filter_type=None):
    # Open video file
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # Using H264 for better quality
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create VideoWriter object with a high-quality codec
    is_color = filter_type != 'grayscale'  # Output in color unless grayscale filter is applied
    # Create VideoWriter object
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), is_color)
    
    # Parse captions from SRT file
    captions = parse_srt(captions_path)
    
    # Define caption properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (255, 255, 255)  # White color
    margin = 10  # Margin from the bottom of the screen
    max_width = width - 2 * margin
    
    # Add captions to each frame
    caption_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply selected filter
        if filter_type:
            frame = add_filters(frame, filter_type)

        # Calculate the current frame's time
        frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        
        # Find the current caption
        while (caption_index < len(captions) and
               frame_time > captions[caption_index]['end_time']):
            caption_index += 1
        
        if (caption_index < len(captions) and
            captions[caption_index]['start_time'] <= frame_time <= captions[caption_index]['end_time']):
            caption_text = captions[caption_index]['text']
        else:
            caption_text = ''
        
        # Wrap text and calculate the position
        lines = wrap_text(caption_text, font, font_scale, font_thickness, max_width)
        y = height - margin
        line_height = cv2.getTextSize('A', font, font_scale, font_thickness)[1]
        
        for line in reversed(lines):
            text_size, _ = cv2.getTextSize(line, font, font_scale, font_thickness)
            text_width = text_size[0]
            text_x = int((width - text_width) / 2)
            if filter_type == 'grayscale':
                cv2.putText(frame, line, (text_x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
            else:
                cv2.putText(frame, line, (text_x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
            y -= (line_height + margin)
        
        # Write the frame
        out.write(frame)
    
    # Release resources
    cap.release()
    out.release()


@app.route("/main", methods=['POST'])
def transcribe():  # put application's code here
    if "file" not in request.files:
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No file part in the request.",
            "status": 400
        }), 400

    file = request.files["file"]
    file_path = f"./temp/{file.filename}"
    # file.save(file_path)
    input_path = file_path

    # TODO: Turn .mp4 to .wav (config/convert_config.py)
    convertedWav = convert_mp4_to_wav(input_path)
    # TODO: Transcribe .wav file to text using AI (config/transcribe_config.py)
    # TODO: Return transcribed text in JSON
    captions_text = process_audio(convertedWav)
    # TODO: Add text to video (config/captions_config.py)
    add_ct = add_captions(input_path, convertedWav, captions_text)
    # TODO: Store in Database (TBD)
    
    # TODO: Return video url
    return add_ct
    # TODO: Delete .wav file ./uploads
    # TODO: Delete .mp4 file from ./temp


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

    return jsonify({"message": "video created!", "video_url": output_file}), 200


if __name__ == '__main__':
    start_time = time.time()
    app.run(debug=True)
    log.info(f"Application started in {time.time() - start_time} seconds")
