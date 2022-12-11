FROM python:3.8.16-slim

ENV PYTHONBUFFERED 1

RUN mkdir /zmall

WORKDIR /zmall

COPY . .

RUN pip install -r requirements.txt