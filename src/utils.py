from __future__ import annotations

from typing import Any, cast

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo


class _FieldInfoProxy:
    """Allows access to ``pydantic.FieldInfo`` attributes plus a name of this field.

    Name is not part of ``pydantic.FieldInfo``, so this proxy provides it. All other
    access is forwarded to the ``pydantic.FieldInfo`` instance.
    """

    def __init__(self, name: str, model_field: FieldInfo):
        self._name = name
        self.field_info = model_field

    def __getattr__(self, key: str) -> Any:
        if key == "name":
            return self._name
        return getattr(self.field_info, key)

    def __repr__(self):
        return self.field_info.__repr__()


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

    def __init__(self, fields: dict[str, FieldInfo]):
        self._fields = fields

    def __getattr__(self, item: str) -> _FieldInfoProxy:
        try:
            return _FieldInfoProxy(item, self._fields[item])
        except KeyError as ex:
            raise AttributeError(f"{item} is not a model field.") from ex


class FieldAccessMeta(ModelMetaclass):
    """Adds static access to ``Pydantic.BaseModel`` fields and nested alias paths.

    See ``_FieldAccessor`` for details.
    """

    @property
    def fields_(cls) -> _FieldAccessor:
        """Static version of ``pydantic.BaseModel.fields``.

        The pydantic implementation is an instance property and doesn't work on classes.
        See ``_FieldAccessor`` for details.
        """
        base_model_cls = cast(BaseModel, cls)
        return _FieldAccessor(fields=base_model_cls.model_fields)
