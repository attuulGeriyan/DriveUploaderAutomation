import os
import mimetypes
import webbrowser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request  # Missing import
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# SCOPES define what access we want
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Define folder name on Drive
TARGET_FOLDER_NAME = "Macbook Pro"

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_folder_id(service, folder_name):
    # Search for the folder by name
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    folders = results.get('files', [])
    if folders:
        return folders[0]['id']
    else:
        # Create folder if it doesn't exist
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

def upload_file(service, file_path, folder_id):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None, None
    
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    # Cache MIME type mapping
    MIME_TYPE_MAP = {
        '.csv': 'application/vnd.google-apps.spreadsheet',
        '.xlsx': 'application/vnd.google-apps.spreadsheet',
        '.xls': 'application/vnd.google-apps.spreadsheet',
        '.docx': 'application/vnd.google-apps.document',
        '.doc': 'application/vnd.google-apps.document'
    }
    
    # Get file extension
    file_ext = os.path.splitext(file_name)[1].lower()
    google_mime = MIME_TYPE_MAP.get(file_ext)
    
    if not google_mime:
        print("Unsupported file type.")
        return None, None

    # Prepare upload metadata
    file_metadata = {
        'name': file_name,
        'mimeType': google_mime,
        'parents': [folder_id]
    }
    
    # Use resumable upload for better reliability
    media = MediaFileUpload(
        file_path, 
        mimetype=mime_type, 
        resumable=True,
        chunksize=1024 * 1024  # 1MB chunks for better performance
    )
    
    # Create file with metadata first
    try:
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = uploaded_file.get('id')
        print(f"Uploaded File ID: {file_id}")
        return file_id, google_mime
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return None, None

def open_in_browser(file_id, google_mime):
    if 'spreadsheet' in google_mime:
        url = f"https://docs.google.com/spreadsheets/d/{file_id}/edit"
    elif 'document' in google_mime:
        url = f"https://docs.google.com/document/d/{file_id}/edit"
    else:
        return
    webbrowser.open(url, new=2)

if __name__ == '__main__':
    file_path = 'test_files/SOP Questionarie.docx'   # Change as needed

    # Check if file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        print("Please check the file path and ensure the file exists.")
        exit(1)

    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    folder_id = get_folder_id(service, TARGET_FOLDER_NAME)
    file_id, google_mime = upload_file(service, file_path, folder_id)
    
    if file_id and google_mime:
        open_in_browser(file_id, google_mime)
    else:
        print("Upload failed.")