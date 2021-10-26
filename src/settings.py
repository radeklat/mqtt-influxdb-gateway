from functools import cache
from typing import Literal, Union

from pydantic import BaseSettings, Field, AnyUrl, IPvAnyAddress


class Settings(BaseSettings):
    """Application config.

    See also:
        - https://docs.influxdata.com/influxdb/cloud/write-data/developer-tools/api/
        - https://docs.influxdata.com/influxdb/cloud/api/#operation/PostWrite
    """

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

    mqtt_server: Union[AnyUrl, IPvAnyAddress]
    mqtt_username: str
    mqtt_password: str

    delay_sec: int


@cache
def get_settings() -> Settings:
    return Settings()
