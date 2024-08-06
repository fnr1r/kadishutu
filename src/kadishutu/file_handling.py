from abc import ABC
from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
from struct import Struct, pack_into, unpack_from
from typing import Any, ClassVar, Callable, Optional, Type, TypeVar, Union
from typing_extensions import Self

from .encryption import decrypt, encrypt


def is_save_decrypted(data: bytearray) -> bool:
    return data[0x40:0x44] == b"GVAS"


@dataclass(repr=False)
class RawSave:
    data: bytearray

    def save(self, path: Path):
        with open(path, "wb") as file:
            file.write(self.data)

    def is_save_decrypted(self) -> bool:
        return is_save_decrypted(self.data)


class EncryptedSave(RawSave):
    @classmethod
    def open(cls, path: Path) -> Self:
        with open(path, "rb") as file:
            return cls(bytearray(file.read()))

    def decrypt(self) -> "DecryptedSave":
        assert not self.is_save_decrypted(), "Save not encrypted"
        return DecryptedSave(bytearray(decrypt(self.data)))


class DecryptedSave(RawSave):
    @classmethod
    def open(cls, path: Path) -> Self:
        with open(path, "rb") as file:
            return cls(bytearray(file.read()))

    @classmethod
    def auto_open(cls, path: Path) -> "DecryptedSave":
        with open(path, "rb") as file:
            data = bytearray(file.read())
        if not is_save_decrypted(data):
            return EncryptedSave(data).decrypt()
        else:
            return cls(data)

    def encrypt(self) -> EncryptedSave:
        assert self.is_save_decrypted(), "Save not decrypted"
        return EncryptedSave(bytearray(encrypt(self.data)))

    def hash_calculate(self):
        return sha1(self.data[0x40:])

    def hash_validate(self) -> bool:
        included_hash = self.data[:20]
        calculated_hash = self.hash_calculate()
        return included_hash == calculated_hash.digest()

    def hash_update(self):
        new_hash = self.hash_calculate()
        data = self.data
        self.data = bytearray(new_hash.digest()) + self.data[20:]
        assert len(data) == len(self.data)

    def save_finished(self, path: Path):
        this = self.encrypt()
        this.save(path)


TBaseEditor = TypeVar("TBaseEditor", bound="BaseEditor")


@dataclass
class BaseMasterEditor(ABC):
    save_data: DecryptedSave

    @property
    def data(self) -> bytearray:
        return self.save_data.data
    @data.setter
    def data(self, data: bytearray):
        self.save_data.data = data

    def dispatch(
        self,
        cls: Callable[..., TBaseEditor],
        *args,
        **kwargs
    ) -> TBaseEditor:
        return cls(self, *args, **kwargs)


@dataclass
class BaseEditor(ABC):
    master: BaseMasterEditor

    @property
    def data(self) -> bytearray:
        return self.master.data
    @data.setter
    def data(self, data: bytearray):
        self.master.data = data

    def dispatch(
        self,
        cls: Callable[..., "TBaseEditor"],
        *args,
        **kwargs
    ) -> "TBaseEditor":
        return cls(self.master, *args, **kwargs)


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
U = TypeVar("U")


def structproperty(
    _: Type[T],
    fmt: Union[str, bytes],
    getter_transformer: Optional[Callable[[U], T]] = None,
    setter_transformer: Optional[Callable[[T], U]] = None,
):
    """
    NOTE: The typing is kinda messed up. I can't really fix this.
    """
    def decorator(func: Callable[..., int]):
        def getter(self) -> T:
            offset = func(self)
            res = unpack_from(fmt, self.data, offset)[0]
            if getter_transformer:
                res = getter_transformer(res)
            return res
        def setter(self, value: T):
            offset = func(self)
            if setter_transformer:
                value = setter_transformer(value)  # type: ignore
            pack_into(fmt, self.data, offset, value)
        return property(getter, setter)
    return decorator
