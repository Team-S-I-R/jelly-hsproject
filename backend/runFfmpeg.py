from flask import Flask, request, send_file
import cv2
import numpy as np
import os
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000", 
    "http://localhost:3001", 
    "http://localhost:3002", 
])

# Lets run through how were adding captions


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

# step 4: add the captions to each frame
def add_captions(input_path, output_path, captions_path):
    # Open video file
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create VideoWriter object
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
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
            cv2.putText(frame, line, (text_x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
            y -= (line_height + margin)
        
        # Write the frame
        out.write(frame)
    
    # Release resources
    cap.release()
    out.release()

# this is the route that actually runs all of the functions
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        # Save the uploaded file
        input_path = 'input_video.mp4'
        file.save(input_path)
        
        # Placeholder for adding captions
        output_path = 'output_video.mp4'
        captions_path = 'captions.srt'  # Adjust this to the path of your captions file
        
        add_captions(input_path, output_path, captions_path)
        
        # Send the processed video file back to the user
        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
