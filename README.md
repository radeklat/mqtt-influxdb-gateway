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

# Environment variables
<!--
    DO NOT EDIT the following section!
    It is auto-generated with settings-doc in CircleCI and committed
    back to the repository on changes.
-->
<!-- settings-doc start -->
## `LOG_LEVEL`

*Optional*, default value: `INFO`

Logging level.

### Possible values

`TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`

## `INFLUXDB_URL`

**Required**

URL of your InfluxDB Cloud instance.
## `INFLUXDB_ORGANIZATION_ID`

**Required**

Organization ID. A hexadecimal string. Should be part of the cloud instance URL or in About Organization. This is not the organization name!
## `INFLUXDB_API_TOKEN`

**Required**

API token with write access to `influxdb_default_bucket`.
## `INFLUXDB_PRECISION`

*Optional*, default value: `ns`

The precision for the unix timestamps within the body line-protocol.

### Possible values

`s`, `ms`, `ns`, `us`

## `INFLUXDB_DEFAULT_BUCKET`

*Optional*

Default value if `{bucket}` in `mqtt_topic_pattern` below is not set or parsed.
## `INFLUXDB_DEFAULT_MEASUREMENT`

*Optional*

Default value if `{measurement}` in `mqtt_topic_pattern` below is not set or parsed.
## `MQTT_HOST`

**Required**

IP address or a host name of an MQTT broker.
## `MQTT_PORT`

*Optional*, default value: `1883`

Port of the MQTT broker.
## `MQTT_USERNAME`

*Optional*

User name used to authenticate with the MQTT broker.
## `MQTT_PASSWORD`

*Optional*

Password used to authenticate with the MQTT broker.
## `MQTT_TOPIC_SUBSCRIBE`

**Required**

A topic to subscribe to. You can also use the '+' and '#' wildcards.
## `MQTT_TOPIC_PATTERN`

**Required**

A pattern to parse the topic into fields sent to InfluxDB. Use `{variable}` or `{variable_type:value}` syntax in topic parts to create the match. Use a plain string to ignore a topic part. The pattern must be a prefix of `mqtt_topic_subscribe`.

When both a variable and a `influxdb_*` configuration option are defined, variable takes precedence.

### Examples

`dt/influxdb/{bucket}/{measurement}/{tag:device_id}/{field}/{value_type}` will parse `dt/influxdb/home/environment/esp8266/temperature/float 23.412` into:

```json
{
   "bucket": "home",
   "measurement": "environment",
   "tags": {"device_id": "esp8266"},
   "fields": {"temperature": 23.412}
}
```

### Possible values

- `{bucket}`: InfluxDB bucket to send data to. Required unless `influxdb_default_bucket` is set.
- `{measurement}`: InfluxDB measurement field. Required unless `influxdb_default_measurement` is set.
- `{field}`: Field name. Required.
- `{value_type}`: Value type used to parse the received data. Optional.
  Acceptable values in the topic are `str`, `int`, `float` and `bool`. Default value is `str`.
- `{tag:TAG_NAME}`: where TAG_NAME will be used as a tag name and the parsed value as a value. Optional.

## `MQTT_MERGE_DATA_POINTS_ON`

*Optional*, default value: `{measurement}{bucket}{tags}`

It is expected there will be a single value in each topic. But InfluxDB allows multiple fields to be sent at once (for example from one device). Use this option to define criteria on which to merge data points. The order and any extra characters aside from variables below are irrelevant. All collected fields are then sent to InfluxDB when any of the fields is seen more than once (suggesting new data is coming in).

### Examples

A value of `{tags[device_id]}` will merge all received data that share the same `device_id` tag.

### Possible values

- `{bucket}`
- `{measurement}`
- `{tags}`: for all tags and their values
- `{tags[NAME]}`: for a value of single tag named `NAME`

<!-- settings-doc end -->

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

- Define what to merge data points on.