from datetime import datetime, timezone
from typing import Any, Dict, Set, Type, Union

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str


_Scalar = Union[str, int, bool, float]


class MergeConflict(Exception):
    pass


class InfluxDBLine(BaseModel):
    measurement: str
    bucket: str
    fields: Dict[str, Any]
    tags: Dict[str, str] = Field(default_factory=dict)
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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

    @property
    def merge_id(self) -> str:
        return f"{self.measurement}/{self.bucket}/{self.tags}"

    def merge(self, other: "InfluxDBLine") -> "InfluxDBLine":
        if not isinstance(other, InfluxDBLine):
            raise TypeError(f"Can only merge instances of '{self.__class__.__name__}' but '{other.__class__}' used.")
        if self.merge_id != other.merge_id:
            raise ValueError("Only instances with identical `merge_id` can be merged.")
        if set(self.fields.keys()).intersection(other.fields.keys()):
            raise MergeConflict("Instances have overlapping fields.")

        model_copy = self.copy(deep=True)
        model_copy.fields.update(other.fields)

        return model_copy

