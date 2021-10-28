from functools import cache
from typing import Literal

from pydantic import BaseSettings, Field, IPvAnyAddress, validator

from constants import LEVEL_DEFAULT, LOG_LEVELS


class Settings(BaseSettings):
    log_level: str = Field(default=LEVEL_DEFAULT)

    # Configuration of access to InfluxDB Cloud.
    influxdb_url: str = Field(..., description="https://.*influxdata.com")
    influxdb_organization_id: str
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

    @validator("log_level")
    def valid_log_level(cls, value, field):
        if value not in LOG_LEVELS:
            raise ValueError(f"'{value}' is not allowed as a value for '{field}'. Allowed values are: {LOG_LEVELS}.")
        return value

@cache
def get_settings() -> Settings:
    return Settings()
