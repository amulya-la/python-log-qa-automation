from datetime import datetime
import os
import shutil
import logging

# Folders
INPUT_FOLDER = "input_files"
VALID_FOLDER = "processed_files/valid"
INVALID_FOLDER = "processed_files/invalid"
LOG_FILE = "logs/automation.log"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def is_valid_qa_file(filename):
    if not filename.startswith("QA_"):
        return False
    parts = filename.split("_", 2)
    if len(parts) < 3:
        return False
    date_part = parts[1]
    try:
        datetime.strptime(date_part, "%Y-%m-%d")
    except ValueError:
        return False
    if not filename.endswith((".txt", ".log")):
        return False
    return True

# Create valid/invalid folders if they don't exist
os.makedirs(VALID_FOLDER, exist_ok=True)
os.makedirs(INVALID_FOLDER, exist_ok=True)

# Move files
for file in os.listdir(INPUT_FOLDER):
    src = os.path.join(INPUT_FOLDER, file)
    if os.path.isfile(src):
        if is_valid_qa_file(file):
            dst = os.path.join(VALID_FOLDER, file)
            shutil.move(src, dst)
            logging.info(f"VALID file moved: {file}")
        else:
            dst = os.path.join(INVALID_FOLDER, file)
            shutil.move(src, dst)
            logging.info(f"INVALID file moved: {file}")
