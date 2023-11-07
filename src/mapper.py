from copy import deepcopy
from typing import Optional, Union

from influx_db import InfluxDBLine, Tag


class TopicToFieldsMapper:
    _SPLIT_CHR = "/"
    _REQUIRED_FIELDS = {
        InfluxDBLine.fields_.bucket.name,
        InfluxDBLine.fields_.measurement.name,
        "field",
    }
    _AVAILABLE_FIELDS = deepcopy(_REQUIRED_FIELDS).union({InfluxDBLine.fields_.tags.name, "value_type"})

    def __init__(self, topic_pattern: str, default_bucket: Optional[str], default_measurement: Optional[str]):
        self._default_kwargs: dict[str, str] = {}
        if default_bucket:
            self._default_kwargs[InfluxDBLine.fields_.bucket.name] = default_bucket
        if default_measurement:
            self._default_kwargs[InfluxDBLine.fields_.measurement.name] = default_measurement
        self._pattern_parts = self._parse_patten(topic_pattern)

    def _parse_patten(self, topic_pattern: str) -> list[Union[str, Tag, None]]:
        parsed_variables: list[Union[str, Tag, None]] = []
        seen_variables: set[str] = set()

        for part in topic_pattern.split(self._SPLIT_CHR):
            if not part or part[0] != "{" or part[-1] != "}":
                parsed_variables.append(None)
                continue  # skip non-patterns
            part = part[1:-1]  # strip brackets
            if part.startswith("tag:"):
                parsed_variables.append(Tag(name=part[4:]))
                seen_variables.add(InfluxDBLine.fields_.tags.name)
            else:
                parsed_variables.append(part)
                seen_variables.add(part)

        if missing_vars := self._REQUIRED_FIELDS.difference(seen_variables.union(self._default_kwargs.keys())):
            raise ValueError(
                f"`mqtt_topic_pattern` set to '{topic_pattern}' is missing one or more "
                f"required variables: {missing_vars}. Make sure they are defined either "
                f"as part of the pattern or as the `influxdb_default_*` settings (if applicable)."
            )

        if unknown_vars := set(seen_variables).difference(self._AVAILABLE_FIELDS):
            raise ValueError(
                f"`mqtt_topic_pattern` set to '{topic_pattern}' contains unknown variable(s): {unknown_vars}"
            )

        return parsed_variables

    def to_influxdb_line(self, topic: str, value: str) -> InfluxDBLine:
        kwargs: dict[str, str] = deepcopy(self._default_kwargs)
        tags: dict[str, str] = {}

        for pattern, part in zip(self._pattern_parts, topic.split(self._SPLIT_CHR)):
            if not pattern:
                continue
            if isinstance(pattern, Tag):
                tags[pattern.name] = part
            else:
                kwargs[pattern] = part

        return InfluxDBLine.from_mqtt(value=value, tags=tags, **kwargs)
