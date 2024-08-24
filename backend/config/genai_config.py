def process_audio(song):
    from pydub import AudioSegment
    from openai import OpenAI

    song = AudioSegment.from_file(song, format="wav")

    ten_minutes = 10 * 60 * 1000

    first_10_minutes = song[:ten_minutes]

    first_10_minutes.export("good_morning_10.wav", format="wav")

    client = OpenAI()

    audio_file = open("speech.wav", "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

    return transcript.words