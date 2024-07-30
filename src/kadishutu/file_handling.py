from abc import ABC, abstractmethod
from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
from struct import Struct, calcsize, pack_into, unpack_from
from typing import Any, ClassVar, Dict, Callable, Optional, Tuple, Type, TypeVar, Union
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


@dataclass
class BaseManager(ABC):
    saveobj: DecryptedSave


TBaseEditor = TypeVar("TBaseEditor", bound="BaseEditor")


@dataclass
class BaseEditor(ABC):
    saveobj: DecryptedSave
    offset: int

    @property
    def data(self) -> bytearray:
        return self.saveobj.data
    @data.setter
    def data(self, data: bytearray):
        self.saveobj.data = data

    def relative_offset(self, relative_offset: int):
        return self.offset + relative_offset

    def delegate(
        self,
        cls: Callable[[DecryptedSave, int], TBaseEditor],
        relative_offset: int
    ) -> TBaseEditor:
        return cls(self.saveobj, self.relative_offset(relative_offset))


@dataclass
class MasterEditor(BaseEditor, ABC):
    saveobj: DecryptedSave
    offset: ClassVar[int] = 0


class BaseStructFieldEditor(BaseEditor, ABC):
    FIELD_FMT: str = NotImplemented

    @property
    def SFMT_LEN(self) -> int:
        return calcsize(self.FIELD_FMT)

    def relative_field_offset(self, no: int) -> int:
        return self.relative_offset(self.SFMT_LEN * no)


class BaseStructEditor(BaseEditor, ABC):
    saveobj: DecryptedSave
    offset: int
    fmt: str = NotImplemented

    @property
    def struct(self) -> Struct:
        return Struct(self.fmt)

    @property
    def size(self) -> int:
        return self.struct.size

    @property
    def raw(self) -> bytes:
        return self.data[self.offset:self.offset+self.size]

    def unpack(self) -> Tuple[Any, ...]:
        return self.struct.unpack_from(self.data, self.offset)

    def pack(self, *v: Any):
        self.struct.pack_into(self.data, self.offset, *v)


class SingularIntEditor(BaseStructEditor, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        struct = self.struct
        empty = bytes([0] * struct.size)
        assert len(struct.unpack(empty)) == 1

    def get(self) -> int:
        return self.unpack()[0]

    def set(self, value: int):
        self.pack(value)

    @property
    @abstractmethod
    def name_table(self) -> Dict[int, str]:
        pass

    @property
    def name(self) -> str:
        return self.name_table[self.get()]


class BaseIdEditor(BaseEditor, ABC):
    _id: int

    @classmethod
    @abstractmethod
    def id_to_offset(cls, id: int) -> int:
        pass

    def __init__(self, saveobj: DecryptedSave, id: int):
        super().__init__(saveobj, self.id_to_offset(id))
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self.offset = self.id_to_offset(value)
        self.id = value


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
