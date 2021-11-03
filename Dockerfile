ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN apt-get --allow-releaseinfo-change update && \
    apt-get install gcc g++ libssl-dev libffi-dev rustc -y && \
    rm -rf /var/lib/apt/*
RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

# PYTHONPATH set after install to prevent bugs
ENV PYTHONPATH="src"

COPY . .

ENTRYPOINT ["poetry", "run", "python", "src/main.py"]
