from copy import deepcopy
from typing import Dict, List, Set, Tuple, Type, Union

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str


_Scalar = Union[str, int, bool, float]


class InfluxDBLine(BaseModel):
    measurement: str
    bucket: str
    field: str
    value: _Scalar
    tags: List[Tuple[str, str]] = Field(default_factory=list)

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
    def from_dict(cls, dictionary: Dict[str, Union[str, List[Tuple[str, str]]]], value: str) -> "InfluxDBLine":
        dict_copy = deepcopy(dictionary)
        dict_copy["value"] = cls._parse_value(dict_copy["value_type"], value)
        dict_copy.pop("value_type")
        return InfluxDBLine(**dict_copy)
