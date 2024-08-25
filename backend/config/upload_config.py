from supabase import create_client
import os

"""
Upload a file to supabase (storage).

:param filepath: The path to the file that needs to be uploaded.
:return: The response from the supabase storage.
"""
url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON')

supabase = create_client(url, key)

def upload_file_to_supabase(filepath: str) -> str:

    with open(filepath, 'rb') as f:
        supabase.storage.from_('video').upload(file=f, path=filepath, file_options={'content-type': 'video/mp4'})

    return f"File uploaded to Supabase: {filepath}"
