#!/bin/sh
cd "$(dirname "$0")"
python3 -m pip install -q flask
python3 app.py
