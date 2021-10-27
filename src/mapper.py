from typing import Dict, List, Union

from influx_db import InfluxDBLine, Tag


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

    def to_infludb_line(self, topic: str, value: str) -> InfluxDBLine:
        output: Dict[str, Union[str, Dict[str, str]]] = {}

        for pattern, part in zip(self._pattern_parts, topic.split(self._SPLIT_CHR)):
            if not pattern:
                continue
            if isinstance(pattern, Tag):
                if "tags" not in output:
                    output["tags"] = {}
                output["tags"][pattern.name] = part
            else:
                output[pattern] = part

        return InfluxDBLine.from_mqtt(value=value, **output)
