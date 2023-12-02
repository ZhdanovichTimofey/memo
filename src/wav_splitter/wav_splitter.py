from pydub import AudioSegment
import os
import shutil

class WavSplitter():
    def __init__(self, audio_path):
        self.audio = AudioSegment.from_wav(audio_path)
        self.dir = self.makedir(audio_path)
    
    @staticmethod
    def makedir(filepath):
        print(filepath)
        dir_path = os.path.splitext(filepath)[0]
        dir_path = r'{}'.format(dir_path)
        
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            
        os.mkdir(dir_path)
        return dir_path
    
    def get_filename(self, indx):
        return os.path.join(self.dir, f'{indx}.wav')
            
    def render(self, data):
        filenames_speakers = []
        
        for id_, [[start, stop], speaker] in enumerate(data):
            start = int(start * 1000)
            stop = int(stop * 1000)
            
            chunk_path = self.get_filename(id_)
            audio_chunk = self.audio[start:stop]
            audio_chunk.export(chunk_path, format="wav")
            filenames_speakers.append((chunk_path, speaker))
        
        return filenames_speakers
