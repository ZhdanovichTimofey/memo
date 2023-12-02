from src.waver.ext_translate import translators

class Waver():
    def __init__(self, ext):
        self.ext = ext

    def to_wav(self, filepath):
        return translators[self.ext](filepath)
    