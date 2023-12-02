from src.utils.tg_parser import get_fileid_and_ext, get_text
from src.utils.tg_requests import send_message
from config.config import UNSUPPORTED_TYPE_MESSAGE, POSSIBLE_EXTENTIONS, START_MESSAGE
import logging

def answer_message(data, chat_id):
    try:
        file_id, ext = get_fileid_and_ext(data)
    except Exception as e:
        logging.error(str(e))
        return False, False
        
    if ext == 'txt' and get_text(data) == '/start':
        send_message(chat_id, START_MESSAGE) 
        return False, False

    if not ext or ext not in POSSIBLE_EXTENTIONS:
        send_message(chat_id, UNSUPPORTED_TYPE_MESSAGE)
        return False, False

    return file_id, ext

