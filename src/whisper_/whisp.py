import sys

import torch
import tqdm
import whisper
import whisper.transcribe

from config.config import CUDA, MODEL_TYPE
from src.utils.tg_requests import send_message


def make_progressbar(chat_id):
    class _CustomProgressBar(tqdm.tqdm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._current = 0  # self.n  # Set the initial value
            self.chat_id = chat_id

        def update(self, n=1):
            super().update(n)
            self._current += n
            message = f"Обработано примерно {round(self._current*100/self.total)}%"
            send_message(self.chat_id, message)
            print(message)

    return _CustomProgressBar


class Whisper:
    def __init__(self):
        self.device = torch.device("cuda" if CUDA else "cpu")
        self.model = whisper.load_model(MODEL_TYPE, device=self.device)
        # self.model.to(self.device)

    def __call__(self, audio_path, chat_id):
        transcribe_module = sys.modules["whisper.transcribe"]
        _CustomProgressBar = make_progressbar(chat_id)
        transcribe_module.tqdm.tqdm = _CustomProgressBar
        # transcribe_module.tqdm.tqdm.chat_id = chat_id

        with torch.no_grad():
            preds = self.model.transcribe(audio_path, language="ru", verbose=None)
        out_text = self.postprocess(preds)
        return out_text

    def postprocess(self, preds):
        text_with_time = []
        for segment in preds["segments"]:
            start = segment["start"]
            end = segment["end"]
            txt = segment["text"]
            text_with_time.append([[start, end], txt])
        return text_with_time
