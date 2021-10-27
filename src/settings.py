from functools import cache
from typing import Literal

from pydantic import BaseSettings, Field, IPvAnyAddress


class Settings(BaseSettings):
    # Configuration of access to InfluxDB Cloud.
    influxdb_url: str = Field(..., description="https://.*influxdata.com")
    influxdb_organization_id: str
    influxdb_bucket: str
    influxdb_measurement: str
    influxdb_api_token: str = Field(
        ..., description="Must be writable into given `influxdb_bucket`."
    )
    influxdb_precision: Literal["s", "ms", "ns", "us"] = Field(
        default="ns",
        description="The precision for the unix timestamps within the body line-protocol.",
    )

    mqtt_host: IPvAnyAddress
    mqtt_port: int = Field(1883, min=1, max=65535)
    mqtt_username: str
    mqtt_password: str
    mqtt_topic_subscribe: str
    mqtt_topic_pattern: str

    delay_sec: int


@cache
def get_settings() -> Settings:
    return Settings()
