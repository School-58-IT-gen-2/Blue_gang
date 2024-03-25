FROM python:3.12-slim

COPY site ./site
COPY game ./game
COPY tg_bot.py ./tg_bot.py
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt