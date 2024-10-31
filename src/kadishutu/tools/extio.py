from abc import ABC
from dataclasses import dataclass
from typing import BinaryIO, Generic, TypeVar, Union

from typing_extensions import Self


MAGIC_ENCODING = "ascii"
ENCODING = "UTF-16"


T = TypeVar("T")


@dataclass
class WrapperClass(Generic[T], ABC):
    _inner: T

    def __getattribute__(self, name: str):
        if name == "_inner":
            return super().__getattribute__(name)
        try:
            return self._inner.__getattribute__(name)
        except AttributeError:
            pass
        return super().__getattribute__(name)

    @classmethod
    def from_parent(cls, io: T) -> Self:
        return cls(io)


class ExtIO(BinaryIO, WrapperClass):
    _inner: BinaryIO

    def skip(self, amount: int):
        self.seek(self.tell() + amount)

    def assert_magic(
        self,
        magic: Union[str, bytes],
        encoding: str = MAGIC_ENCODING
    ):
        if isinstance(magic, str):
            magic = magic.encode(encoding)
        assert isinstance(magic, bytes)
        data = self.read(len(magic))
        assert data == magic, f"Invalid magic {data!r} instead of {magic!r}"

    def read_u32_le(self) -> int:
        return int.from_bytes(self.read(4), byteorder="little")

    def read_chars(self, amount: int, encoding: str = ENCODING) -> str:
        return self.read(amount).decode(encoding)

    def read_until_null(self) -> str:
        return b''.join(iter(lambda: self.read(1), b'\0')).decode()

    def read_utf16_le_until_null(self) -> str:
        return b''.join(iter(lambda: self.read(2), b'\0\0')).decode("UTF-16-LE")
