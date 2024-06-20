FROM python:3.11-alpine
WORKDIR /main
RUN apk update
RUN apk add git
COPY ./requirements.txt ./setup.py ./README.md /main/
COPY ./discordai /main/discordai
COPY ./discordAI-modelizer /main/discordAI-modelizer
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir .
RUN pip3 install --no-cache-dir ./discordAI-modelizer && rm -R /main/*
