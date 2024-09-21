import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from django.conf import settings
load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDS_FILE = os.path.join(settings.BASE_DIR, "fileUpload","client-credentials.json")

def deleteFile(fileId):
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    service.files().delete(fileId=fileId).execute()
    print("FILE DELETED SUCCESSFULLY")
    return True
