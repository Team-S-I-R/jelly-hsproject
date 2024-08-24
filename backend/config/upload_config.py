from supabase import create_client
import os

def upload_file_to_supabase(filepath):

    url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON')

    supabase = create_client(url, key)
    # response = supabase.storage().create_bucket('avatars')
    # if response.error:
    #     raise Exception(response.error.message)

    with open(filepath, 'rb') as f:
        supabase.storage.from_('video').upload(file=f, path='path_on_supastorage', file_options={'content-type': 'video/mp4'})

    return f'File uploaded to Supabase: {filepath}'