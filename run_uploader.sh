#!/bin/bash
# Navigate to the script directory
cd /Users/attuulgeriyan/Documents/Projects/DriveUploaderAutomation

# Ensure all dependencies are installed
/Users/attuulgeriyan/Documents/Projects/DriveUploaderAutomation/venv/bin/pip install -r requirements.txt

# Run the Python script in the background with nohup
nohup /Users/attuulgeriyan/Documents/Projects/DriveUploaderAutomation/venv/bin/python auto_uploader_watcher.py > uploader.log 2>&1 &
echo "Uploader started and running in background. Check uploader.log for details."
