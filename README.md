# Drive Uploader Automation

Automated system that monitors your Downloads folder for new files and uploads them to Google Drive.

## Features

- Monitors Downloads folder for new files
- Supports common document formats (CSV, XLSX, DOCX, DOC, XLS)
- Automatic upload to specified Google Drive folder
- Opens uploaded files in browser after successful upload
- Real-time file system monitoring using watchdog
- Error handling and logging

## Requirements

- Python 3.x
- Google Drive API credentials
- Required packages listed in requirements.txt

## Setup

1. Clone the repository:


2. Create a virtual environment (recommended):


3. Install dependencies:


4. Set up Google Drive API:
   - Go to Google Cloud Console (https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable Google Drive API
   - Create OAuth 2.0 credentials for a Desktop App:
     - Go to APIs & Services > Credentials
     - Click "Create Credentials" > "OAuth client ID"
     - Select "Desktop app" as the application type
     - Give it a name (e.g., "Drive Uploader")
     - Click Create
     - Download the JSON file and save it as `credentials.json` in your project root directory

5. Run the application once to generate `token.json`:
   - The first run will open a browser window asking for Google Drive authorization
   - After authorization, the `token.json` file will be automatically created

## Usage

Run the uploader:


Or use the shell script:


## Supported File Types

- .csv
- .xlsx
- .docx
- .doc
- .xls

## License

[Add your license information here]
