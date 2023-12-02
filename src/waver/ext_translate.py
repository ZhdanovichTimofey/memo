from config.config import FRAMERATE 
from config.config import TMP_FOLDER
import shutil
import subprocess
import os

def get_filename(filepath):
    filename_ext = os.path.split(filepath)[-1]
    filename = os.path.splitext(filename_ext)[0]
    
    wav_filepath = os.path.join(TMP_FOLDER, filename + '.wav')
    
    if os.path.isfile(wav_filepath):
        os.remove(wav_filepath)
    
    return os.path.abspath(os.path.join(TMP_FOLDER, filename + '.wav'))


def mp3_translate(filepath):
    
    wav_filepath = get_filename(filepath)
    
    subprocess.run(
        ['ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le', '-ar', str(FRAMERATE), wav_filepath]
    )

    return wav_filepath
    
def mp4_translate(filepath):
    wav_filepath = get_filename(filepath)
    
    subprocess.run(
        ['ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le', '-ar', str(FRAMERATE), wav_filepath]
    )
    return wav_filepath
    
def ogg_translate(filepath):
    wav_filepath = get_filename(filepath)
    
    subprocess.run(
        ['ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le', '-ar', str(FRAMERATE), wav_filepath]
    )
    return wav_filepath

def aac_translate(filepath):
    wav_filepath = get_filename(filepath)
    
    subprocess.run(
        ['ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le', '-ar', str(FRAMERATE), wav_filepath]
    )
    return wav_filepath
    

def copy(filepath):
    wav_filepath = get_filename(filepath)
    shutil.copy(filepath, wav_filepath)
    return wav_filepath

translators = {
    'mp3': mp3_translate,
    'wav': copy,
    'mp4': mp4_translate,
    'ogg': ogg_translate,
    'aac': aac_translate
}    