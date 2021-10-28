import sys
from typing import Dict

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from loguru import logger
from paho.mqtt.client import Client as MQTTClient
from paho.mqtt.client import MQTTMessage
from pydantic import BaseModel, Field

from constants import LOGGING_FORMAT
from influx_db import InfluxDBLine, MergeConflict
from mapper import TopicToFieldsMapper
from settings import get_settings


class UserData(BaseModel):
    influxdb_client: InfluxDBClient
    topic_to_fields: TopicToFieldsMapper
    data_aggregator: Dict[str, InfluxDBLine] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


def on_connect(client: MQTTClient, userdata: UserData, flags, result_code: int) -> None:
    """The callback for when the client receives a CONNACK response from the server.

    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
    """
    del userdata, flags
    logger.info(f"Connected with result code {result_code}.")
    client.subscribe(get_settings().mqtt_topic_subscribe)


def on_message(client: MQTTClient, userdata: UserData, message: MQTTMessage) -> None:
    """The callback for when a PUBLISH message is received from the server."""
    del client
    line = userdata.topic_to_fields.to_infludb_line(message.topic, message.payload)
    merge_id = line.merge_id

    logger.debug("Single measurement received.", line=line)

    try:
        userdata.data_aggregator[merge_id] = userdata.data_aggregator[merge_id].merge(line)
    except KeyError:
        userdata.data_aggregator[merge_id] = line
    except MergeConflict:
        write_to_influxdb(userdata.influxdb_client, userdata.data_aggregator.pop(merge_id))
        userdata.data_aggregator[merge_id] = line


def write_to_influxdb(client: InfluxDBClient, data: InfluxDBLine) -> None:
    with client.write_api(write_options=ASYNCHRONOUS) as write_api:
        write_api.write(bucket=data.bucket, record=data.dict())
    logger.debug("Data sent to InfluxDB", data=data)


def main() -> None:
    settings = get_settings()

    logger.configure(handlers=[])  # removes all pre-existing handlers
    logger.add(sys.stdout, format=LOGGING_FORMAT, level=settings.log_level, backtrace=True)

    user_data = UserData(
        topic_to_fields=TopicToFieldsMapper(settings.mqtt_topic_pattern),
        influxdb_client=InfluxDBClient(
            url=settings.influxdb_url,
            token=settings.influxdb_api_token,
            org=settings.influxdb_organization_id,
        ),
    )

    mqtt_client = MQTTClient(client_id=None)
    mqtt_client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)
    mqtt_client.user_data_set(user_data)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(host=str(settings.mqtt_host), port=settings.mqtt_port)

    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Exiting.")


if __name__ == "__main__":
    main()
