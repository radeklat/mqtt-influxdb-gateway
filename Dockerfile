ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN apt-get --allow-releaseinfo-change update && \
    apt-get install gcc g++ libssl-dev libffi-dev -y && \
    rm -rf /var/lib/apt/*
RUN python -m pip install --upgrade pip

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install "cryptography<3.5" poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

# PYTHONPATH set after install to prevent bugs
ENV PYTHONPATH="src"

COPY . .

ENTRYPOINT ["poetry", "run", "python", "src/main.py"]
