import os
from config.config import DOWNLOAD_FOLDER, TMP_FOLDER

def save_file(responce, file_name):
    filepath = os.path.join(DOWNLOAD_FOLDER, file_name)
    with open(filepath, 'wb') as file:
        file.write(responce.content)
    
    return filepath

def save_to_txt(text, file_name):
    filepath = os.path.join(TMP_FOLDER, file_name)
    
    with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)

    return open(filepath, 'rb')