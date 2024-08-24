# this take in the wav file
def process_audio(song):
    from pydub import AudioSegment
    from openai import OpenAI

    song = AudioSegment.from_file(song, format="wav")

    ten_minutes = 10 * 60 * 1000

    first_10_minutes = song[:ten_minutes]

    first_10_minutes.export("good_morning_10.wav", format="wav")

  # Export the first 10 minutes to a new file
    temp_wav_path = "processed_10_minutes.wav"
    first_10_minutes.export(temp_wav_path, format="wav")

    client = OpenAI()

# Transcribe the processed file
# opening the file
    with open(temp_wav_path, "rb") as audio_file:
        # creating the transcription
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
    )
        
    # make the words object look like 

    # give example

    
        
    print("Transcript: ", transcript)
    return transcript.words