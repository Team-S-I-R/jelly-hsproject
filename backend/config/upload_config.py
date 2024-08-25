from supabase import create_client
import os
import uuid
import time

"""
Upload a file to supabase (storage) and store the public URL in the database.

:param filepath: The path to the file that needs to be uploaded.
:param filename: The name of the file to be stored.
:return: The response from the supabase storage.
"""
url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON')

supabase = create_client(url, key)

def generate_random_id() -> str:
    return str(uuid.uuid4())

def upload_file_to_supabase(filepath: str, filename: str) -> str:

    suppath = "thefiles/" + filename

    with open(filepath, 'rb') as f:
        supabase.storage.from_('video').upload(file=f, path=suppath, file_options={'content-type': 'video/mp4'})

    time.sleep(1)
    # Get the public URL of the uploaded file
    public_url = supabase.storage.from_('video').get_public_url(suppath)

    # Generate a random ID for the database entry
    random_id = generate_random_id()

    # Store the public URL in the database
    supabase.table('Url').insert({'id': random_id, 'url': public_url}).execute()

    return f"File uploaded to Supabase: {filepath}, Public URL: {public_url}"
