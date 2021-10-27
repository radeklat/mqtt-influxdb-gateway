from typing import Any, Dict, List, Tuple, Type, Union

from loguru import logger
# from influxdb_client import InfluxDBClient, Point
# from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from pydantic import BaseModel, Field, validator, PrivateAttr

from settings import get_settings


class Tag(BaseModel):
    name: str


class Fields(BaseModel):
    measurement: str
    bucket: str
    field: str
    value_type: Type
    tags: List[Tuple[str, str]] = Field(default_factory=list)

    _VALID_TYPES: Dict[str, Type] = {
        "str": str,
        "int": int,
        "bool": bool,
        "float": float,
    }

    @validator("value_type", pre=True)
    def _transform_type(cls, value: str, field: Field) -> Type:
        if value not in cls._VALID_TYPES:
            raise ValueError(
                f"'{value}' is not a valid value for '{field.name}'. Allowed values are: {cls._VALID_TYPES.keys()}."
            )
        return cls._VALID_TYPES[value]


class TopicToFieldsMapper:
    _SPLIT_CHR = "/"

    def __init__(self, topic_pattern: str):
        self._pattern_parts = self._parse_patten(topic_pattern)

    def _parse_patten(self, topic_pattern: str) -> List[Union[str, Tag, None]]:
        pattern_parts: List[Union[str, Tag, None]] = []

        for part in topic_pattern.split(self._SPLIT_CHR):
            if not part or part[0] != "{" or part[-1] != "}":
                pattern_parts.append(None)
                continue  # skip non-patterns
            part = part[1:-1]  # strip brackets
            if part.startswith("tag:"):
                pattern_parts.append(Tag(name=part[4:]))
            else:
                pattern_parts.append(part)

        return pattern_parts

    def to_dict(self, topic: str) -> Fields:
        output: Dict[str, Union[str, List[Tuple[str, str]]]] = {}

        for pattern, part in zip(self._pattern_parts, topic.split(self._SPLIT_CHR)):
            if not pattern:
                continue
            if isinstance(pattern, Tag):
                if "tags" not in output:
                    output["tags"] = []
                output["tags"].append((pattern.name, part))
            else:
                output[pattern] = part

        return Fields(**output)


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
    print(f"{userdata.topic_to_fields.to_dict(message.topic)} {message.payload}")


def main() -> None:
    settings = get_settings()

    user_data = UserData(
        topic_to_fields=TopicToFieldsMapper(settings.mqtt_topic_pattern),
    )

    client = MQTTClient(client_id=None)
    client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)
    client.user_data_set(user_data)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host=str(settings.mqtt_host), port=settings.mqtt_port)
    client.loop_forever()

    # client = InfluxDBClient(
    #     url=settings.influxdb_url,
    #     token=settings.influxdb_api_token,
    #     org=settings.influxdb_organization_id,
    # )
    #
    # write_api = client.write_api(write_options=SYNCHRONOUS)
    #
    # p = Point(settings.influxdb_measurement).tag("device_type", "esp8266").tag("device_id", "df_4d_87_0a_0b_49").field("temperature", 25.3)
    #
    # write_api.write(bucket=settings.influxdb_bucket, record=p)


if __name__ == "__main__":
    main()
