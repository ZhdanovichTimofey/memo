import os
from dotenv import load_dotenv
from config.utils.ConfigExceptions import EnvNotFoundException

def load_env():
    dotenv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(dotenv_path, '.env')
    
    print(dotenv_path)
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else: 
        raise EnvNotFoundException()