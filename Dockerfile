FROM python:3.12.6-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt