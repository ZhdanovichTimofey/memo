from pyngrok import ngrok
import requests

from config.config import TELEGRAM_TOKEN

def start_ngrok():
    http_tunnel = ngrok.connect(
        addr="localhost:5000",
    )
    print(http_tunnel.public_url)
    return http_tunnel.public_url


def set_webhook(url):
    r = requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook', 
        headers={"Content-Type" : "application/json"},
        json={'url': url}
    )
    print(r.text)
    

def setup_tg():
    set_webhook(start_ngrok())

    