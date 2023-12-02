class NotValidExtentionException(Exception):
    def __init__(self, needed_ext, actual_ext):
        

        self.message = f'There no {needed_ext} in this data. There {actual_ext} extention'

        if not actual_ext:
            self.message = f'There no {needed_ext} in this data. There no found extention in this data'

        super().__init__(self.message)
        
class TooBigFile(Exception):
    def __init__(self):
        self.message = f'File is too big'
        super().__init__(self.message)