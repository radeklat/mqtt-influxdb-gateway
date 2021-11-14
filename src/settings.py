from functools import cache
from typing import Literal, Optional

from pydantic import BaseSettings, Field, validator

from constants import LEVEL_DEFAULT, LOG_LEVELS


class Settings(BaseSettings):
    log_level: str = Field(default=LEVEL_DEFAULT, description="Logging level.", possible_values=LOG_LEVELS)

    # Configuration of access to InfluxDB Cloud.
    influxdb_url: str = Field(
        ..., description="URL of your InfluxDB Cloud instance.", regex=r"https://.*\.influxdata.com"
    )
    influxdb_organization_id: str = Field(
        ...,
        description="Organization ID. A hexadecimal string. Should be part of the cloud "
        "instance URL or in About Organization. This is not the organization name!",
    )
    influxdb_api_token: str = Field(..., description="API token with write access to `influxdb_default_bucket`.")
    influxdb_precision: Literal["s", "ms", "ns", "us"] = Field(
        default="ns", description="The precision for the unix timestamps within the body line-protocol."
    )
    influxdb_default_bucket: Optional[str] = Field(
        None, description="Default value if `{bucket}` in `mqtt_topic_pattern` below is not set or parsed."
    )
    influxdb_default_measurement: Optional[str] = Field(
        None, description="Default value if `{measurement}` in `mqtt_topic_pattern` below is not set or parsed."
    )

    mqtt_host: str = Field(..., description="IP address or a host name of an MQTT broker.")
    mqtt_port: int = Field(1883, min=1, max=65535, description="Port of the MQTT broker.")
    mqtt_username: Optional[str] = Field(None, description="User name used to authenticate with the MQTT broker.")
    mqtt_password: Optional[str] = Field(None, description="Password used to authenticate with the MQTT broker.")
    mqtt_topic_subscribe: str = Field(
        ..., description="A topic to subscribe to. You can also use the '+' and '#' wildcards."
    )
    mqtt_topic_pattern: str = Field(
        ...,
        description="A pattern to parse the topic into fields sent to InfluxDB. "
        "Use `{variable}` or `{variable_type:value}` syntax in topic parts to create the "
        "match. Use a plain string to ignore a topic part. The pattern must be a prefix of "
        "`mqtt_topic_subscribe`.\n"
        "\n"
        "When both a variable and a `influxdb_*` configuration option are defined, variable takes precedence.",
        possible_values=[
            ("{bucket}", "InfluxDB bucket to send data to. Required unless `influxdb_default_bucket` is set."),
            ("{measurement}", "InfluxDB measurement field. Required unless `influxdb_default_measurement` is set."),
            ("{field}", "Field name. Required."),
            (
                "{value_type}",
                "Value type used to parse the received data. Optional.\n  Acceptable values in the topic are "
                "`str`, `int`, `float` and `bool`. Default value is `str`.",
            ),
            ("{tag:TAG_NAME}", "where TAG_NAME will be used as a tag name and the parsed value as a value. Optional."),
        ],
        example="`dt/influxdb/{bucket}/{measurement}/{tag:device_id}/{field}/{value_type}` "
        "will parse `dt/influxdb/home/environment/esp8266/temperature/float 23.412` into:\n"
        "\n"
        "```json\n"
        "{\n"
        '   "bucket": "home",\n'
        '   "measurement": "environment",\n'
        '   "tags": {"device_id": "esp8266"},\n'
        '   "fields": {"temperature": 23.412}\n'
        "}\n"
        "```",
    )
    mqtt_merge_data_points_on: str = Field(
        default="{measurement}{bucket}{tags}",
        description="It is expected there will be a single value in each topic. But "
        "InfluxDB allows multiple fields to be sent at once (for example from one device). "
        "Use this option to define criteria on which to merge data points. The order and "
        "any extra characters aside from variables below are irrelevant. All collected fields "
        "are then sent to InfluxDB when any of the fields is seen more than once (suggesting "
        "new data is coming in).",
        possible_values=[
            ("{bucket}",),
            ("{measurement}",),
            ("{tags}", "for all tags and their values"),
            ("{tags[NAME]}", "for a value of single tag named `NAME`"),
        ],
        example="A value of `{tags[device_id]}` will merge all received data that share the same `device_id` tag.",
    )

    @validator("log_level")
    def valid_log_level(cls, value, field):  # pylint: disable=no-self-argument, no-self-use
        if value not in LOG_LEVELS:
            raise ValueError(f"'{value}' is not allowed as a value for '{field}'. Allowed values are: {LOG_LEVELS}.")
        return value


@cache
def get_settings() -> Settings:
    return Settings()
