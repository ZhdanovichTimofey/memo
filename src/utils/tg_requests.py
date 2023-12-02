import requests
from config.config import TELEGRAM_TOKEN, POSSIBLE_EXTENTIONS, POSSIBLE_TYPES
from src.utils.exceptions import TooBigFile
import os

__all__ = ['get_file', 'send_message']

req = {
    'POST': requests.post,
    'GET': requests.get
}

def _make_request(method, param_name=None, param_val=None, req_type='POST', data=None):
    
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}'
    
    if param_name is not None and param_val is not None:
        url += f'?{param_name}={param_val}'
    resp = req[req_type](url, data=data)    
    return resp

def _download_request(filepath):
    url = f'https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{filepath}'
    print(url)
    return req['GET'](url)


def _get_filepath_and_name(json_data) -> tuple:
    filepath = json_data['result']['file_path']
    filename = os.path.split(filepath)[-1]
    return filepath, filename


def get_chat_id(json_data):
    return json_data["message"]["chat"]["id"]


def get_file(file_id):
    resp = _make_request(
        method='getFile',
        param_name='file_id',
        param_val=file_id
    )
    
    if resp.json().get('error_code') == 400:
        raise TooBigFile()
    
    print('a', resp.json())

    file_path, file_name = _get_filepath_and_name(resp.json())
    
    print(file_path, file_name)

    resp = _download_request(file_path)

    return resp, file_name

def send_message(chat_id, text):
    _make_request(
        method='SendMessage',
        data={"chat_id": chat_id, "text": text}
    )
    

def get_file_id(json_data):
    if not any([type_ in json_data["message"] for type_ in POSSIBLE_TYPES]):
        return False
    
    for type_ in POSSIBLE_TYPES:
        if type_ in json_data['message']:
            file_name = json_data['message'][type_]['file_name']
            
            extention = file_name.split('.')[-1]
            
            if extention in POSSIBLE_EXTENTIONS:
                file_id = json_data['message'][type_]['file_id']
                return file_id
            
    return False

def send_document(filestream, chat_id, caption='This is your transcribation'):
    send_document = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument?'
    data = {
        'chat_id': chat_id,
        'parse_mode':'HTML',
        'caption': caption
    }
    
    files = {
        'document': filestream
    }

    r = requests.post(send_document, data=data, files=files, stream=True)

    filestream.close()

    return r.json()