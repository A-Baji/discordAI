FROM python:3.11-alpine
WORKDIR /main
RUN apk update
RUN apk add git
COPY ./requirements.txt ./setup.py ./README.md /main/
COPY ./discordai /main/discordai
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir . && rm -R /main/*
