from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from struct import Struct
from typing import (
    Any, ClassVar, Generic, Optional, Tuple, Type, TypeVar, Union, overload,
)

from typing_extensions import Self

from kadishutu.tools.fdatetime import (
    python_to_unreal_datetime, unreal_to_python_datetime
)

from .file_handling import DecryptedSave


TBaseEditor = TypeVar("TBaseEditor", bound="BaseEditor")


class AbstractEditor(ABC):
    data: bytearray

    @abstractmethod
    def dispatch(
        self,
        cls: Type[TBaseEditor],
        *args,
        **kwargs
    ) -> TBaseEditor:
        raise NotImplementedError


@dataclass
class BaseMasterEditor(AbstractEditor, ABC):
    save_data: DecryptedSave

    @property
    def data(self) -> bytearray:
        return self.save_data.data
    @data.setter
    def data(self, data: bytearray):
        self.save_data.data = data

    def dispatch(
        self,
        cls: Type[TBaseEditor],
        *args,
        **kwargs
    ) -> TBaseEditor:
        return cls(self, *args, **kwargs)


@dataclass
class BaseEditor(AbstractEditor, ABC):
    master: BaseMasterEditor

    @property
    def data(self) -> bytearray:
        return self.master.data
    @data.setter
    def data(self, data: bytearray):
        self.master.data = data

    def dispatch(
        self,
        cls: Type[TBaseEditor],
        *args,
        **kwargs
    ) -> "TBaseEditor":
        return cls(self.master, *args, **kwargs)

    @classmethod
    def disp(cls, *args, **kwargs):
        return AbsoulteDispatcher(cls, *args, **kwargs)


TBaseDynamicEditor = TypeVar("TBaseDynamicEditor", bound="BaseDynamicEditor")


class BaseOffsetEditor(BaseEditor, ABC):
    master: BaseMasterEditor
    offset: int

    def relative_as_absolute_offset(self, relative_offset: int):
        return self.offset + relative_offset

    def relative_dispatch(
        self,
        cls: Type[TBaseDynamicEditor],
        relative_offset: int,
        *args,
        **kwargs
    ) -> TBaseDynamicEditor:
        return self.dispatch(
            cls,
            self.relative_as_absolute_offset(relative_offset),
            *args,
            **kwargs
        )


class BaseStaticEditor(BaseOffsetEditor, ABC):
    offset: ClassVar[int] = NotImplemented

    @classmethod
    def __init_subclass__(cls):
        if issubclass(cls, ABC):
            return
        if getattr(cls, "offset") == NotImplemented:
            raise NotImplementedError(
                f"Class {cls} lacks required offset class attribute"
            )


@dataclass
class BaseDynamicEditor(BaseOffsetEditor, ABC):
    offset: int

    @classmethod
    def rdisp(cls, *args, **kwargs):
        return RelativeDispatcher(cls, *args, **kwargs)

    @classmethod
    def fdisp(cls, *args, **kwargs):
        return RelativeDispatcher(cls, *args, **kwargs)


class BaseStructEditor(BaseOffsetEditor, ABC):
    struct: Union[str, bytes] = NotImplemented

    @classmethod
    def __init_subclass__(cls):
        if issubclass(cls, ABC):
            return
        if getattr(cls, "struct") == NotImplemented:
            raise NotImplementedError(
                f"Class {cls} lacks required offset class attribute"
            )

    @property
    def struct_obj(self) -> Struct:
        return Struct(self.struct)

    def struct_unpack(self, relative_offset: int) -> Any:
        return self.struct_obj.unpack_from(
            self.data,
            self.relative_as_absolute_offset(relative_offset)
        )

    def struct_pack(self, relative_offset: int, *args) -> Any:
        self.struct_obj.pack_into(
            self.data,
            self.relative_as_absolute_offset(relative_offset),
            *args
        )


class BaseStructAsFieldEditor(BaseStructEditor, ABC):
    def field_as_relative_offset(self, field_offset: int) -> int:
        return self.struct_obj.size * field_offset

    def field_as_absolute_offset(self, field_offset: int):
        return self.offset + self.field_as_relative_offset(field_offset)

    def field_dispatch(
        self,
        cls: Type[TBaseDynamicEditor],
        field_offset: int,
        *args,
        **kwargs
    ) -> TBaseDynamicEditor:
        return self.relative_dispatch(
            cls,
            self.field_as_relative_offset(field_offset),
            *args,
            **kwargs
        )


class BaseStructAsSingularValueEditor(BaseStructEditor, ABC):
    @property
    def value(self) -> Any:
        return self.struct_unpack(0)[0]

    @value.setter
    def value(self, v: Any):
        self.struct_pack(0, v)


T = TypeVar("T")
TAbstractEditor = TypeVar("TAbstractEditor", bound=AbstractEditor)


class EditorGetter(Generic[T, TAbstractEditor], ABC):
    roffset: int
    _editor: Optional[TAbstractEditor]

    def __init__(self, offset: int):
        self.roffset = offset
    
    @property
    def editor(self) -> TAbstractEditor:
        assert self._editor
        return self._editor
    
    @property
    def offset(self) -> int:
        if isinstance(self.editor, BaseOffsetEditor):
            return self.editor.offset + self.roffset
        else:
            return self.roffset

    @property
    def data(self) -> bytearray:
        return self.editor.data

    @abstractmethod
    def read(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def write(self, value: T):
        raise NotImplementedError

    @overload
    def __get__(self, instance: object, _) -> T: ...
    @overload
    def __get__(self, instance: None, _) -> Self: ...
    def __get__(self, instance, _):
        if instance is None:
            return self
        assert instance is not None
        assert isinstance(instance, AbstractEditor)
        self._editor = instance # type: ignore
        res = self.read()
        self._editor = None
        return res

    def __set__(self, instance, value: T):
        assert instance is not None
        assert isinstance(instance, AbstractEditor)
        self._editor = instance # type: ignore
        self.write(value)
        self._editor = None


TBaseEditor = TypeVar("TBaseEditor", bound=BaseEditor)


class AbsoulteDispatcher(EditorGetter, Generic[TBaseEditor]):
    def __init__(self, ed_cls: Type[TBaseEditor], *args, **kwargs):
        self.ed_cls = ed_cls
        self.args = args
        self.kwargs = kwargs

    def read(self):
        return self.editor.dispatch(
            self.ed_cls,
            *self.args,
            **self.kwargs,
        )

    def write(self, _):
        raise AttributeError("dispatchers are read-only")

    def __get__(self, instance, _) -> TBaseEditor:
        return super().__get__(instance, _)

    def __set__(self, _, v):
        self.write(v)


TBaseDynamicEditor = TypeVar("TBaseDynamicEditor", bound=BaseDynamicEditor)


class RelativeDispatcher(AbsoulteDispatcher, Generic[TBaseDynamicEditor]):
    ed_cls: Type[TBaseDynamicEditor]

    def __init__(
        self,
        ed_cls: Type[TBaseDynamicEditor],
        relative_offset: int,
        *args,
        **kwargs
    ):
        super().__init__(ed_cls, *args, **kwargs)
        self.relative_offset = relative_offset
    
    @property
    def editor(self) -> BaseOffsetEditor:
        return super().editor

    def read(self):
        return self.editor.relative_dispatch(
            self.ed_cls,
            self.relative_offset,
            *self.args,
            **self.kwargs,
        )

    def __get__(self, instance, _) -> TBaseDynamicEditor:
        return super().__get__(instance, _)


class FieldDispatcher(AbsoulteDispatcher, Generic[TBaseDynamicEditor]):
    ed_cls: Type[TBaseDynamicEditor]

    def __init__(
        self,
        ed_cls: Type[TBaseDynamicEditor],
        field: int,
        *args,
        **kwargs
    ):
        super().__init__(ed_cls, *args, **kwargs)
        self.field = field
    
    @property
    def editor(self) -> BaseStructAsFieldEditor:
        return super().editor

    def read(self):
        return self.editor.field_dispatch(
            self.ed_cls,
            self.field,
            *self.args,
            **self.kwargs
        )

    def __get__(self, instance, _) -> TBaseDynamicEditor:
        return super().__get__(instance, _)


class BytesEditor(EditorGetter):
    size: int

    def __init__(self, offset: int, size: int):
        super().__init__(offset)
        self.size = size

    @property
    def end_offset(self) -> int:
        return self.offset + self.size

    def read(self) -> bytearray:
        return self.data[self.offset:self.end_offset]

    def write(self, value: bytearray):
        assert len(value) == self.size
        self.data[self.offset:self.end_offset] = value


class BitEditor(EditorGetter):
    bit: int

    def __init__(self, offset: int, bit: int):
        super().__init__(offset)
        self.bit = bit

    @property
    def bit_value(self) -> int:
        return 1 << self.bit

    @property
    def inverse_bit_value(self) -> int:
        return 0xff - self.bit_value

    def read(self) -> bool:
        return bool(self.data[self.offset] & self.bit_value)

    def write(self, value: bool):
        raw = self.data[self.offset]
        if value:
            res = raw | self.bit_value
        else:
            res = raw & self.inverse_bit_value
        self.data[self.offset] = res


STRUCT_FMT = Union[str, bytes]


class StructEditor(EditorGetter):
    fmt: STRUCT_FMT = NotImplemented

    @property
    def struct_obj(self) -> Struct:
        return Struct(self.fmt)

    def read(self) -> Tuple[Any, ...]:
        return self.struct_obj.unpack_from(self.data, self.offset)
    
    def write(self, v: Tuple[Any, ...]):
        self.struct_obj.pack_into(self.data, self.offset, *v)


class SingularStructEditor(StructEditor):
    def read(self) -> Any:
        return super().read()[0]
    
    def write(self, v: Any):
        super().write((v,))


class IntEditor(SingularStructEditor):
    def read(self) -> int:
        return super().read()
    
    def write(self, v: int):
        super().write(v)


class U8Editor(IntEditor):
    fmt = "<B"


class BoolEditor(U8Editor):
    def read(self) -> bool:
        return bool(super().read())
    
    def write(self, v: bool):
        super().write(int(v))


class U16Editor(IntEditor):
    fmt = "<H"


class I16Editor(IntEditor):
    fmt = "<h"


class U32Editor(IntEditor):
    fmt = "<I"


class U64Editor(IntEditor):
    fmt = "<Q"


TEnum = TypeVar("TEnum", bound=Enum)


class EnumEditor(SingularStructEditor, Generic[TEnum]):
    def __init__(self, offset: int, enum: Type[TEnum], fmt: STRUCT_FMT = "<B"):
        super().__init__(offset)
        self.fmt = fmt
        self.enum = enum

    def read(self) -> TEnum:
        return self.enum(super().read())
    
    def write(self, v: TEnum):
        super().write(v.value)


class TimeDeltaEditor(U32Editor):
    def read(self) -> timedelta:
        return timedelta(seconds=super().read())
    
    def write(self, v: timedelta):
        super().write(v.seconds)


class UnrealTimeEditor(U64Editor):
    def read(self) -> datetime:
        return unreal_to_python_datetime(super().read())
    
    def write(self, v: datetime):
        super().write(python_to_unreal_datetime(v))
