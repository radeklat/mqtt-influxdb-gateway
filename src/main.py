from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from settings import get_settings


def main() -> None:
    settings = get_settings()

    client = InfluxDBClient(
        url=settings.influxdb_url,
        token=settings.influxdb_api_token,
        org=settings.influxdb_organization_id,
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = Point(settings.influxdb_measurement).tag("device_type", "esp8266").tag("device_id", "df_4d_87_0a_0b_49").field("temperature", 25.3)

    write_api.write(bucket=settings.influxdb_bucket, record=p)


if __name__ == "__main__":
    main()
