FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3-full wget

WORKDIR /workarea
COPY . /workarea
WORKDIR /workarea/client
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt


