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
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Drive API
   - Create credentials (OAuth 2.0 Client ID)
   - Download credentials.json

5. Run the setup script:


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
