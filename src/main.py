from loguru import logger
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from pydantic import BaseModel

from mapper import TopicToFieldsMapper
from settings import get_settings


class UserData(BaseModel):
    topic_to_fields: TopicToFieldsMapper

    class Config:
        arbitrary_types_allowed = True


def on_connect(client: MQTTClient, userdata: UserData, flags, rc: int) -> None:
    """The callback for when the client receives a CONNACK response from the server.

    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
    """
    del userdata, flags
    logger.info(f"Connected with result code {rc}.")
    client.subscribe(get_settings().mqtt_topic_subscribe)


def on_message(client: MQTTClient, userdata: UserData, message: MQTTMessage) -> None:
    """The callback for when a PUBLISH message is received from the server."""
    del client
    print(str(userdata.topic_to_fields.to_infludb_line(message.topic, message.payload)))


def main() -> None:
    settings = get_settings()

    user_data = UserData(
        topic_to_fields=TopicToFieldsMapper(settings.mqtt_topic_pattern),
    )

    mqtt_client = MQTTClient(client_id=None)
    mqtt_client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)
    mqtt_client.user_data_set(user_data)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(host=str(settings.mqtt_host), port=settings.mqtt_port)
    mqtt_client.loop_forever()

    influxdb_client = InfluxDBClient(
        url=settings.influxdb_url,
        token=settings.influxdb_api_token,
        org=settings.influxdb_organization_id,
    )

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    p = Point(settings.influxdb_measurement).tag("device_type", "esp8266").tag("device_id", "df_4d_87_0a_0b_49").field("temperature", 25.3)

    write_api.write(bucket=settings.influxdb_bucket, record=p)


if __name__ == "__main__":
    main()
