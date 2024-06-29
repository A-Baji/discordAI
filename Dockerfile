ARG PY_VER
FROM python:${PY_VER}
WORKDIR /main
COPY ./requirements.txt ./setup.py ./README.md /main/
COPY ./discordai /main/discordai
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir . && rm -R /main/*
