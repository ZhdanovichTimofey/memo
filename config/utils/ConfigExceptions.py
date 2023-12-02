class VarNotFoundException(Exception):
    def __init__(self, var_name):
        self.message = f'{var_name} not found in .env file'
        super().__init__(self.message)

class EnvNotFoundException(Exception):
    def __init__(self):
        self.message = '.env file not found in config directory'
        super().__init__(self.message)
        