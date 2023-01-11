FROM python:3.8.16-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /zmall

WORKDIR /zmall

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt