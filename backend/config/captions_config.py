import cv2
import re


def parse_srt(srt_path):
    """
    Parse the SRT file into a list of tuples with start time, end time, and caption text.

    :param srt_path: The path provided to the SRT file.
    :return: A list of dictionaries with keys 'start_time', 'end_time', and 'text'.
    """
    captions = []
    with open(srt_path, 'r') as file:
        srt_content = file.read()

        blocks = srt_content.strip().split('\n\n')
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                time_range = lines[1]
                start_time, end_time = time_range.split(' --> ')
                caption_text = ' '.join(lines[2:])

                captions.append({
                    'start_time': convert_srt_time_to_seconds(start_time),
                    'end_time': convert_srt_time_to_seconds(end_time),
                    'text': caption_text
                })

    return captions


def convert_srt_time_to_seconds(srt_time):
    """
    Convert SRT time format (HH:MM:SS,MMM) to seconds.

    :param srt_time: The SRT time string.
    :return: The time in seconds (float).
    """
    h, m, s, ms = map(int, re.split('[:,]', srt_time))
    return int(h) * 3600 + int(m) * 60 + int(s) + int(srt_time.split(',')[1]) / 1000


def wrap_text(text, font, font_scale, font_thickness, max_width):
    """
    Wrap text to fit within a given width.

    :param text: The text that needs to be wrapped.
    :param font: The font used to render the text.
    :param font_scale: The scale of the font.
    :param font_thickness: The thickness of the font.
    :param max_width: The maximum width of the
    :return: A list[str] of lines of text that fit within the given width.
    """
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


def add_filters(frame, filter_type='grayscale'):
    """
    Applies a filter to the frame.

    :param frame: The frame to apply the filter to.
    :param filter_type: The filter to apply to the frame.
    :return: The frame with the filter applied, otherwise the original frame.
    """
    if filter_type == 'grayscale':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'blur':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_type == 'edge_detection':
        return cv2.Canny(frame, 100, 200)
    else:
        return frame  # No filter applied


def add_captions(input_path, output_path, captions_path, filter_type=None):
    cap = cv2.VideoCapture(input_path)

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    is_color = filter_type != 'grayscale'
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), is_color)

    captions = parse_srt(captions_path)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0  # Increase the font scale to make the text bigger
    font_thickness = 3  # Increase the font thickness to make the text thicker
    color = (255, 255, 255)
    border_color = (0, 0, 0)  # Black border color
    margin = 20  # Increase the margin to add more space between lines
    max_width = width - 2 * margin

    caption_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if filter_type:
            frame = add_filters(frame, filter_type)

        frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        while caption_index < len(captions) and frame_time > captions[caption_index]['end_time']:
            caption_index += 1

        if (caption_index < len(captions) and
                captions[caption_index]['start_time'] <= frame_time <= captions[caption_index]['end_time']):
            caption_text = captions[caption_index]['text']
        else:
            caption_text = ''

        lines = wrap_text(caption_text, font, font_scale, font_thickness, max_width)
        y = height - margin
        line_height = cv2.getTextSize('A', font, font_scale, font_thickness)[1]

        for line in reversed(lines):
            text_size, _ = cv2.getTextSize(line, font, font_scale, font_thickness)
            text_width = text_size[0]
            text_x = int((width - text_width) / 2)
            
            # Draw the border
            cv2.putText(frame, line, (text_x, y - 60), font, font_scale, border_color, font_thickness + 2, cv2.LINE_AA)
            # Draw the text
            cv2.putText(frame, line, (text_x, y - 60), font, font_scale, color, font_thickness, cv2.LINE_AA)
            y -= (line_height + margin)

        out.write(frame)

    cap.release()
    out.release()

    return output_path
