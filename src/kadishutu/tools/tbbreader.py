from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Generic, List, TypeVar
from typing_extensions import Self


MAGIC_ENCODING = "ascii"
ENCODING = "UTF-16"
UEXP_OFFSET = 0x25


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

    def read_chars(self, amount: int) -> str:
        return self.read(amount).decode(MAGIC_ENCODING)

    def read_u32_le(self) -> int:
        return int.from_bytes(self.read(4), byteorder="little")


@dataclass
class Tbl:
    table_size: int
    row_size: int
    rows: List[bytes]
    MAGIC = "TBL1"

    @property
    def row_amount(self) -> int:
        (res, chk) = divmod(self.table_size, self.row_size)
        assert chk == 0
        return res

    @classmethod
    def open(cls, file: ExtIO, offset: int) -> Self:
        if file.tell() != offset:
            file.seek(offset)
        assert file.read_chars(4) == cls.MAGIC
        table_size = file.read_u32_le()
        row_size = int.from_bytes(file.read(4), byteorder="little")
        file.skip(4)
        this = cls(table_size, row_size, [])
        for _ in range(this.row_amount):
            this.rows.append(file.read(this.row_size))
        return this


@dataclass
class Tbcr:
    tables: List[Tbl]
    MAGIC = "TBCR"

    @classmethod
    def _open(cls, file: ExtIO, start_offset: int = 0) -> Self:
        file.seek(start_offset)
        assert file.read_chars(4) == cls.MAGIC
        header_size = file.read_u32_le()
        table_amount = file.read_u32_le()
        table_offsets = [
            file.read_u32_le() + header_size + start_offset
            for _ in range(table_amount)
        ]
        tables = [
            Tbl.open(file, offset)
            for offset in table_offsets
        ]
        return cls(tables)

    @classmethod
    def open(cls, file: BinaryIO, start_offset: int = 0) -> Self:
        return cls._open(ExtIO.from_parent(file), start_offset)

    @classmethod
    def from_path(cls, path: Path, start_offset: int = 0) -> Self:
        if not start_offset and path.name.endswith(".uexp"):
            start_offset = UEXP_OFFSET
        return cls.open(path.open("rb"), start_offset)
