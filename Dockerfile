ARG PY_VER
FROM python:${PY_VER}
WORKDIR /main
COPY ./requirements.txt ./setup.py ./README.md /main/
COPY ./discordai /main/discordai
COPY ./discordAI-modelizer /main/discordAI-modelizer
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir .
RUN pip3 install --no-cache-dir ./discordAI-modelizer -U && rm -R /main/*
