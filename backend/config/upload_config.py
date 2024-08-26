from supabase import create_client
import os
import uuid
import time
from dotenv import load_dotenv
import subprocess


load_dotenv()
def compress_video(input_file_path, output_file_path):
    command = [
        'ffmpeg', '-i', input_file_path, '-vcodec', 'libx264', '-crf', '28', output_file_path
    ]
    subprocess.run(command, capture_output=True, check=True)
    return output_file_path

"""
Upload a file to supabase (storage) and store the public URL in the database.

:param filepath: The path to the file that needs to be uploaded.
:param filename: The name of the file to be stored.
:return: The response from the supabase storage.
"""
url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
# do not change this
key = os.getenv('NEXT_PUBLIC_SUPABASE_SERVICE_ROLE')
supabase = create_client(url, key)


def generate_random_id() -> str:
    """
    Generate a random ID using the UUID lib.

    :return: A random provided ID.
    """
    return str(uuid.uuid4())


def upload_file_to_supabase(filepath: str, filename: str) -> str:
    """
    Upload a file to Supabase (storage) and store the public URL in the database.
    :param filepath: The path to the file that needs to be uploaded.
    :param filename: The name of the file that needs to be uploaded.
    :return: The response from the Supabase storage.
    """

    temp_dir = "./temp/"
    compressed_filepath = compress_video(filepath, temp_dir + os.path.basename(filepath)[:-4] + (filename) + ".mp4")

    suppath = "theFiles/" + os.path.basename(compressed_filepath)

    with open(f'./temp/captioned_video{filename}.mp4', 'rb') as f:
        supabase.storage.from_('video').upload(file=f, path=suppath, file_options={'content-type': 'video/mp4'})

    time.sleep(1)
    # Get the public URL of the uploaded file
    public_url = supabase.storage.from_('video').get_public_url(suppath)

    # Generate a random ID for the database entry
    random_id = generate_random_id()

    # Store the public URL in the database
    supabase.table('Url').insert({'id': random_id, 'url': public_url}).execute()

    return public_url
