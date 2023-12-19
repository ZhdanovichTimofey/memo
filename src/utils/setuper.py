import requests
from pyngrok import ngrok

from config.config import TELEGRAM_TOKEN
from config.config import NGROK_AUTH_TOKEN


def start_ngrok():
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    http_tunnel = ngrok.connect(
        addr="localhost:5000",
        authtoken_from_env=True
    )
    print(http_tunnel.public_url)
    return http_tunnel.public_url


def set_webhook(url):
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
        headers={"Content-Type": "application/json"},
        json={"url": url},
    )
    print(r.text)


def setup_tg():
    set_webhook(start_ngrok())
