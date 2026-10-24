"""Локальный сервер для игры «Миша не может учиться».

Запуск: двойной клик по start.bat (Windows) или start.command (macOS),
либо вручную:
    pip install flask
    python app.py
Браузер с игрой откроется сам: http://127.0.0.1:5000

С телефона: подключи его к тому же Wi-Fi, что и компьютер, и открой адрес
«С телефона», который сервер напишет при запуске. Если не открывается —
разреши Python входящие подключения в брандмауэре.
"""
import socket
import threading
import webbrowser
from pathlib import Path

from flask import Flask, send_from_directory

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.route("/three.min.js")
def three():
    return send_from_directory(ROOT, "three.min.js")


@app.route("/models/list.json")
def models_list():
    # игра грузит только существующие модели — без 404 в консоли
    files = sorted(f.name for f in (ROOT / "models").glob("*.glb"))
    return {"files": files}


@app.route("/models/<path:name>")
def models(name):
    return send_from_directory(ROOT / "models", name)


def lan_ip():
    # адрес компьютера в локальной сети (пакеты никуда не отправляются)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return None


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    ip = lan_ip()
    print(f"Игра на этом компьютере: {url}")
    if ip:
        print(f"С телефона (тот же Wi-Fi): http://{ip}:5000")
    print("Остановить — Ctrl+C")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    # 0.0.0.0 — чтобы телефон в той же сети мог открыть игру
    app.run(host="0.0.0.0", port=5000, debug=False)
