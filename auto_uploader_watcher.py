import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from drive_uploader import authenticate, get_folder_id, upload_file, open_in_browser

# Path to monitor
DOWNLOADS_PATH = os.path.expanduser("~/Downloads")
SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".docx", ".doc", ".xls")
TARGET_FOLDER_NAME = "Macbook Pro"

class FileHandler(FileSystemEventHandler):
    def __init__(self, service, folder_id):
        self.service = service
        self.folder_id = folder_id

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.endswith(SUPPORTED_EXTENSIONS):
            print(f"\n📄 New file detected: {file_path}")
            time.sleep(1)  # wait briefly to ensure the file is done downloading
            try:
                file_id, google_mime = upload_file(self.service, file_path, self.folder_id)
                open_in_browser(file_id, google_mime)
            except Exception as e:
                print(f"⚠️ Error uploading {file_path}: {e}")

def start_watching():
    print(f"👀 Watching folder: {DOWNLOADS_PATH}")
    creds = authenticate()
    service = build_drive_service(creds)
    folder_id = get_folder_id(service, TARGET_FOLDER_NAME)

    event_handler = FileHandler(service, folder_id)
    observer = Observer()
    # Configure observer with optimized settings
    observer.schedule(
        event_handler, 
        path=DOWNLOADS_PATH, 
        recursive=False
    ) 
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def build_drive_service(creds):
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=creds)

if __name__ == "__main__":
    start_watching()
