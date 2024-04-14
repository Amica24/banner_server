FROM --platform=linux/amd64 python:3.8.10-slim as base

RUN apt-get -y update \
    && apt-get install -y wget gnupg unzip curl
RUN apt-get -y update

WORKDIR /srv
RUN apt-get update \
    && apt-get --no-install-recommends install -y gcc g++ libpq-dev python3-dev libfreetype6-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip==23.0.1
RUN pip install watchdog[watchmedo]
RUN pip install mypy
EXPOSE 8765

COPY ./requirements.txt ./
RUN pip install -U pip==23.0.1 --no-cache-dir --no-deps -r ./requirements.txt

RUN mkdir -p ./logs

COPY ./banner_service .

ENV PYTHONPATH=/srv/deps:/srv:/usr/local/bin:/srv/deps/bin
