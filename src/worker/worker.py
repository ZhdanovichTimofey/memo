import logging
import os

from config.config import (DONE_MESSAGE, DOWNLOAD_FILE_MESSAGE,
                           RUN_DIARIZATOR_MESSAGE, RUN_WAV_SPLITTER_MESSAGE,
                           SETUP_DIARIZATOR_MESSAGE,
                           START_TRANSCRIBATION_MESSAGE,
                           TOO_BIG_FILE_ERROR_MESSAGE)
from src.combiner.combiner import Combiner
from src.diarizator.diarizator import Diarizator
from src.downloader.downloader import Downloader
from src.summarizer.summarizer import Summarizer
from src.utils.exceptions import TooBigFile
from src.utils.file_funcs import save_to_txt, save_to_docx
from src.utils.tg_requests import send_document, send_message
from src.wav_splitter.wav_splitter import WavSplitter
from src.waver.waver import Waver


class Worker:
    def __init__(self, task, model):
        self.file_id = task["file_id"]
        self.ext = task["ext"]
        self.chat_id = task["chat_id"]
        self.lock = task["lock"]
        self.is_running = False

        self.model = model
        self.downloader = Downloader(self.file_id)
        self.waver = Waver(self.ext)

    def run(self):

        self.is_running = True

        try:
            filepath = self.download()
            filepath = self.to_wav(filepath)
        except TooBigFile as e:
            self.is_running = False
            send_message(self.chat_id, TOO_BIG_FILE_ERROR_MESSAGE)
            print(str(e))
            logging.info(self.chat_id, str(e))
            return False

        self.lock.acquire()

        try:
            timeslices_by_speaker = self.diarization(filepath)
        except Exception as e:
            send_message(
                self.chat_id, "Что то пошло не так с диаризацией, попробуйте заново"
            )
            self.is_running = False
            self.lock.release()
            print(str(e))
            logging.info(self.chat_id, str(e))
            return False

        try:
            text_with_time = self.transcribe(filepath)

        except Exception as e:
            send_message(
                self.chat_id, "Что то пошло не так с транскрибацией, попробуйте заново"
            )
            self.is_running = False
            self.lock.release()
            print(str(e))
            logging.info(self.chat_id, str(e))
            return False

        try:
            combined_text = self.combine(timeslices_by_speaker, text_with_time)

            text = "\n".join(
                [f"{speaker} : {replic}" for (replic, speaker) in combined_text]
            )
            self.send_text(filepath, text, summary=False)

            summarized_text = self.summarize(combined_text)

            text_questions = self.quests(combined_text)

        except Exception as e:
            self.is_running = False
            self.lock.release()
            send_message(
                self.chat_id, "Что то пошло не так c суммаризацией, попробуйте заново"
            )
            print(str(e))
            logging.info(self.chat_id, str(e))
            return False

        self.lock.release()
        print(summarized_text)
        self.send_text(filepath, summarized_text, summary=True)

        print(text_questions)
        self.send_text(filepath, text_questions, summary=False, questions=True)

        self.is_running = False

    def summarize(self, combined_text):
        summarizer = Summarizer(combined_text)
        summary = summarizer.summarize()
        return summary

    def quests(self, combined_text):
        summarizer = Summarizer(combined_text)
        questions = summarizer.get_questions()
        return questions

    def combine(self, diarization, text_with_time):
        combiner = Combiner(diarization, text_with_time)
        combined_text = combiner.combine()
        return combined_text

    def download(self):
        send_message(self.chat_id, DOWNLOAD_FILE_MESSAGE)
        return self.downloader.download_file()

    def diarization(self, filepath):
        send_message(self.chat_id, SETUP_DIARIZATOR_MESSAGE)
        diarizator = Diarizator(filepath)

        send_message(self.chat_id, RUN_DIARIZATOR_MESSAGE)
        timeslices_by_speaker = diarizator.render()
        return timeslices_by_speaker

    def to_wav(self, filepath):
        return self.waver.to_wav(filepath)

    def split_wav(self, timeslices_by_speaker, filepath):
        wav_splitter = WavSplitter(filepath)
        send_message(self.chat_id, RUN_WAV_SPLITTER_MESSAGE)
        filepaths_speakers = wav_splitter.render(timeslices_by_speaker)
        return filepaths_speakers

    def transcribe(self, filepath):
        send_message(self.chat_id, START_TRANSCRIBATION_MESSAGE)
        text_with_time = self.model(filepath, self.chat_id)
        send_message(self.chat_id, DONE_MESSAGE)
        return text_with_time

    def send_text(self, filepath, text, summary=False, questions=False):
        dir, filename = os.path.split(filepath)
        filename, ext = os.path.splitext(filename)
        caption = "Ваша полная транскрибация"
        if summary:
            filename += "_summary"
            caption = "Краткое резюме"
            filename += ".docx"
            send_document(save_to_docx(text, filename), self.chat_id, caption)
        elif questions:
            filename += "_questions"
            caption = "Вопросы по тексту"
            filename += ".docx"
            send_document(save_to_docx(text, filename), self.chat_id, caption)
        else:
            filename += ".txt"

            send_document(save_to_txt(text, filename), self.chat_id, caption)
