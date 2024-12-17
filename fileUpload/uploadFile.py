import os
import json
from google.oauth2.service_account import Credentials
from . getSubFolderId import createGetSubfolder
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from dotenv import load_dotenv
import os
from django.conf import settings
load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDS_FILE = json.loads(os.getenv('DRIVE_CLIENT_CREDENTIAL'))


def uploadFileToDrive(file_name, document_type, file):
    # Authenticate using service account credentials
    print(CREDS_FILE)
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    print("HELLO1")
    service = build('drive', 'v3', credentials=creds)
    print("HELLO2")
    subfolder_name = ''
    if document_type == 'gym_logo':
        subfolder_name = 'gym_logo'
    elif document_type == 'gym_certificate':
        subfolder_name = 'gym_certificate'
    elif document_type == 'gym_license':
        subfolder_name = 'gym_license'
    
    subfolder_id = createGetSubfolder(service, os.getenv('GOOGLE_DRIVE_PARENT_ID'), subfolder_name)
    print("HELLO3")
    file_metadata = {
        'name': file_name,
        'parents': [subfolder_id]
    }
    print("HELLO4", file_metadata)
    file_stream = BytesIO(file.read())
    print("hello5")
    media = MediaIoBaseUpload(file_stream, mimetype=file.content_type)
    print("hello6")
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = uploaded_file.get('id')
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    print("hello7")
    service.permissions().create(fileId=file_id, body=permission).execute()
    shareable_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    print("hello8")
    return shareable_url, file_id

