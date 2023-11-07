from datetime import datetime, timezone
from typing import Any, ClassVar, Union

from pydantic import BaseModel, Field

from utils import FieldAccessMeta


class Tag(BaseModel):
    name: str


_Scalar = Union[str, int, bool, float]


class MergeConflict(Exception):
    pass


class InfluxDBLine(BaseModel, metaclass=FieldAccessMeta):
    measurement: str
    bucket: str
    fields: dict[str, Any]
    tags: dict[str, str] = Field(default_factory=dict)
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    _VALID_TYPES: set[type] = {str, int, bool, float}
    _VALID_TYPE_NAMES: dict[str, type] = {_.__name__: _ for _ in _VALID_TYPES}

    _merge_on: ClassVar[str] = ""

    @classmethod
    def _parse_value(cls, value_type: str, value: str) -> _Scalar:
        if value_type not in cls._VALID_TYPE_NAMES:
            raise ValueError(
                f"'{value_type}' is not a valid value for 'value_type'. "
                f"Allowed values are: {list(cls._VALID_TYPE_NAMES.keys())}."
            )
        return cls._VALID_TYPE_NAMES[value_type](value)

    @classmethod
    def from_mqtt(
        cls,
        measurement: str,
        bucket: str,
        tags: dict[str, str],
        field: str,
        value: str,
        value_type: str = "str",
    ) -> "InfluxDBLine":
        return InfluxDBLine(
            measurement=measurement,
            bucket=bucket,
            fields={field: cls._parse_value(value_type, value)},
            tags=tags,
        )

    @classmethod
    def merge_data_points_on(cls, new_pattern: str) -> None:
        """Merge instances with identical string formatted using ``self.__dict__.`."""
        cls._merge_on = new_pattern

    @property
    def merge_id(self) -> str:
        return self._merge_on.format(**self.__dict__)

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
