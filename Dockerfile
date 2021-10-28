FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock* ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get --allow-releaseinfo-change update && \
    apt-get install gcc g++ -y && \
    pip install -U pip && \
    pip install poetry && \
    poetry install --no-dev --no-root && \
    apt-get remove gcc g++ -y && \
    apt-get autoremove -y && \
    apt-get clean

# PYTHONPATH set after install to prevent bugs
ENV PYTHONPATH="src"

COPY . .

ENTRYPOINT python src/main.py
