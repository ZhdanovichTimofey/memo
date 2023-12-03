import logging
from threading import Semaphore

from flask import Flask, request

from src.scheduler.scheduler import Scheduler
from src.utils.message_answerer import answer_message
from src.utils.setuper import setup_tg
from src.utils.tg_requests import send_message
from src.whisper_.whisp import Whisper

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")

model = Whisper()
schedule = Scheduler(model)
lock = Semaphore()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]

        print(request.json)
        logging.info(str(request.json))

        file_id, ext = answer_message(request.json, chat_id)

        if file_id and ext:
            task = {"file_id": file_id, "ext": ext, "chat_id": chat_id, "lock": lock}
            schedule.add(task)

            if len(schedule.get_active_workers()) - 1:
                text = (
                    f"Перед вами в очереди "
                    f"{len(schedule.get_active_workers()) - 1} человек"
                )
                send_message(
                    chat_id,
                    text,
                )

    return {"ok": True}


if __name__ == "__main__":
    setup_tg()
    app.run(debug=False)
