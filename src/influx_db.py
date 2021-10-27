from typing import Dict, Set, Type, Union

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str


_Scalar = Union[str, int, bool, float]


class InfluxDBLine(BaseModel):
    measurement: str
    bucket: str
    fields: Dict[str, _Scalar]
    tags: Dict[str, str] = Field(default_factory=dict)

    _VALID_TYPES: Set[Type] = {str, int, bool, float}
    _VALID_TYPE_NAMES: Dict[str, Type] = {_.__name__: _ for _ in _VALID_TYPES}

    @classmethod
    def _parse_value(cls, value_type: str, value: str) -> _Scalar:
        if value_type not in cls._VALID_TYPE_NAMES:
            raise ValueError(
                f"'{value_type}' is not a valid value for 'value_type'. "
                f"Allowed values are: {cls._VALID_TYPE_NAMES.keys()}."
            )
        return cls._VALID_TYPE_NAMES[value_type](value)

    @classmethod
    def from_mqtt(
        cls, measurement: str, bucket: str, tags: Dict[str, str], field: str, value_type: str, value: str
    ) -> "InfluxDBLine":
        return InfluxDBLine(
            measurement=measurement, bucket=bucket, fields={field: cls._parse_value(value_type, value)}, tags=tags
        )
