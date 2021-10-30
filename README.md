<h1 align="center" style="border-bottom: none;">:chart_with_downwards_trend:&nbsp;&nbsp; MQTT ⇒ InfluxDB Gateway &nbsp;&nbsp;:chart_with_upwards_trend:</h1>
<h3 align="center">An MQTT gateway sending data to InfluxDB</h3>

<p align="center">
    <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/radeklat/mqtt-influxdb-gateway">
    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/radeklat/mqtt-influxdb-gateway">
    <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/radeklat/mqtt-influxdb-gateway">
    <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2021">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/radeklat/mqtt-influxdb-gateway">
    <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/radeklat/mqtt-influxdb-gateway">
    <img alt="Docker Image Version (latest semver)" src="https://img.shields.io/docker/v/radeklat/mqtt-influxdb-gateway?label=image%20version">
    <img alt="Docker Image Size (latest semver)" src="https://img.shields.io/docker/image-size/radeklat/mqtt-influxdb-gateway">
</p>

# Installation

## As a script

1. Open terminal
2. Make sure [`git`](https://github.com/git-guides/install-git) is installed:
   ```shell script
   git --version   
   ```
   The output should look something like:
   ```text
   git version 2.25.1
   ```
3. Make sure Python 3.9+ is installed:
   ```shell script
   python --version
   ```
   The output should look something like:
   ```text
   Python 3.9.7
   ```
   * If it shows `2.7.x` instead, try `python3` instead and use it in the rest of the guide.
   * If it shows `3.8.x` or lower, use [`pyenv`](https://github.com/pyenv/pyenv#installation) to install a higher version of Python on your system.
4. Make sure [`poetry`](https://python-poetry.org/docs/#installation) is installed:
   ```shell script
   poetry --version
   ```
   The output should look something like:
   ```
   Poetry version 1.1.5
5. Clone this repository:
   ```shell script
   git clone https://github.com/radeklat/mqtt-influxdb-gateway.git
   cd mqtt-influxdb-gateway
   ```
6. Copy the `.env.template` file into `.env` file:
   ```shell script
   cp .env.template .env
   ```
7. Edit the `.env` file, fill all missing values and/or change existing ones to suit your needs.
8. Install all application dependencies:
   ```shell script
   poetry install --no-dev
   ```
9. Run the app:
    ```shell script
    poetry run python src/main.py
    ```

## As a docker container

1. Open terminal
2. Make sure [`docker`](https://docs.docker.com/get-docker/) is installed:
   ```shell script
   docker --version   
   ```
   The output should look something like:
   ```text
   Docker version 20.10.5, build 55c4c88
   ```
3. Create a base folder structure for the service:
   ```shell script
   cd mqtt-influxdb-gateway
   # Download .env file template
   curl https://raw.githubusercontent.com/radeklat/mqtt-influxdb-gateway/main/.env.template --output .env
   ```
4. Edit the `.env` file and fill the missing details.
5. Run the container:
   ```shell script
   docker run \
      --pull always --rm --name mqtt-influxdb-gateway \
      --env-file=.env \
      radeklat/mqtt-influxdb-gateway:latest
   ```
   This configuration will run the service in the foreground (you need to keep the terminal open) and always use the latest version.
   * Change `latest` to [a specific version](https://hub.docker.com/repository/registry-1.docker.io/radeklat/mqtt-influxdb-gateway/tags) if you don't always want the latest version or remove the `--pull always` flag to not update.


Add `--detach` flag to run in the background. You can close the terminal, but it will not start on system start up.
* To see the log of the service running in the background, run `docker logs mqtt-influxdb-gateway`
* To stop the service, run `docker container stop mqtt-influxdb-gateway`

## As a service

You can use the above-mentioned docker image to run the sync as a service on server or even your local machine. The simples way is to use docker compose:

1. Make sure you have [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed:
   ```shell script
   docker --version
   docker-compose --version
   ```
   The output should look something like:
   ```text
   Docker version 20.10.5, build 55c4c88
   docker-compose version 1.28.5, build unknown
   docker-py version: 4.4.4
   CPython version: 3.8.5
   OpenSSL version: OpenSSL 1.1.1f  31 Mar 2020
   ```
2. Create a base folder structure for the service:
   ```shell script
   mkdir mqtt-influxdb-gateway 
   cd mqtt-influxdb-gateway
   ```
3. Download a compose file and an example .env file:
   ```shell script
   BASE_URL=https://raw.githubusercontent.com/radeklat/mqtt-influxdb-gateway/main
   curl $BASE_URL/.env.template --output .env
   curl $BASE_URL/docker-compose.yml -O
   ```
4. Edit the `.env` file and fill the missing details.
5. Run the service:
   ```shell script
   docker-compose up
   ```
   This command will run the service in the foreground (you need to keep the terminal open) and always use the latest version.
   * Change `latest` to [a specific version](https://hub.docker.com/repository/registry-1.docker.io/radeklat/mqtt-influxdb-gateway/tags) if you don't always want the latest version.


Add `--detach` flag to run in the background. You can close the terminal. The service should start on system start up.
* To see the log of the service running in the background, run `docker-compose logs mqtt-influxdb-gateway`
* To stop the service, run `docker-compose stop mqtt-influxdb-gateway`

# Update

## As a script

1. Open terminal
2. Navigate to the project repository:
   ```shell script
   cd mqtt-influxdb-gateway
   ```
3. Update the source code:
   ```shell script
   git pull
   ```

4. Update application dependencies:
   ```shell script
   poetry install --no-dev
   ```
5. Run the application again.

## From docker-compose

If you used the `latest` tag, run `docker-compose pull mqtt-influxdb-gateway`.

# Development

## Building for ARMv7

At the moment, build for ARMv7 takes about 15-20 minutes. This is caused by the cryptography package switching to Rust compiler (some info [here](https://github.com/matrix-org/synapse/issues/9403)). The build process is significantly slower and not suitable for running in the free tier CircleCI build pipeline.

To build and push the image manually, run:

```shell script
inv docker-build
```

## Paho documentation

https://github.com/eclipse/paho.mqtt.python#contents

## InfluxDB documentation

- https://docs.influxdata.com/influxdb/cloud/write-data/developer-tools/api/
- https://docs.influxdata.com/influxdb/cloud/api/#operation/PostWrite

# TODOs

- Multi-stage docker build (356.17 MB -> 125.53 MB)
