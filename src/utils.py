from __future__ import annotations

from typing import ClassVar, Dict

from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass


class _FieldAccessor:
    """Allows static access to ``pydantic.BaseModel`` fields.

    You can access field attributes via ``Model.fields_.<field>.<attribute>``. Note the
    difference between ``fields`` and ``fields_``. ``fields`` is already defined on
    ``pydantic.BaseModel`` but it is an instance property and doesn't work on classes.

    Example:
        >>> from pydantic import BaseModel
        >>> class MyModel(BaseModel, metaclass=FieldAccessMeta):
        >>>     created_date: str
        >>> print(MyModel.fields_.created_date.name)
        "created_date"
    """

    def __init__(self, fields: Dict[str, ModelField]):
        self._fields = fields

    def __getattr__(self, item: str) -> ModelField:
        try:
            return self._fields[item]
        except KeyError as ex:
            raise AttributeError(f"{item} is not a model field.") from ex


class FieldAccessMeta(ModelMetaclass):
    """Adds static access to ``Pydantic.BaseModel`` fields and nested alias paths.

    See ``_FieldAccessor`` for details.
    """

    __fields__: ClassVar[dict]

    @property
    def fields_(cls) -> _FieldAccessor:
        """Static version of ``pydantic.BaseModel.fields``.

        The pydantic implementation is an instance property and doesn't work on classes.
        See ``_FieldAccessor`` for details.
        """
        return _FieldAccessor(fields=cls.__fields__)
