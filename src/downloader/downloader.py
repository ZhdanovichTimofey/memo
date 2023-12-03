import os

from config.config import DOWNLOAD_FOLDER
from src.utils.tg_requests import get_file


class Downloader:
    def __init__(self, file_id):
        self.file_id = file_id

    def download_file(self):

        responce, filename = get_file(self.file_id)

        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(filepath, "wb") as file:
            file.write(responce.content)

        return filepath
