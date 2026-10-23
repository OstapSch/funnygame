"""Локальный сервер для игры «Миша не может учиться».

Запуск: двойной клик по start.bat (Windows) или start.command (macOS),
либо вручную:
    pip install flask
    python app.py
Браузер с игрой откроется сам: http://127.0.0.1:5000
"""
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


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Игра: {url}  (остановить — Ctrl+C)")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
