from src.utils.tg_requests import get_file
from src.utils.exceptions import TooBigFile
from config.config import DOWNLOAD_FOLDER
import os

class Downloader():
    def __init__(self, file_id):
        self.file_id = file_id

    def download_file(self):
        
        responce, filename = get_file(self.file_id)
        
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(filepath, 'wb') as file:
            file.write(responce.content)
        
        return filepath