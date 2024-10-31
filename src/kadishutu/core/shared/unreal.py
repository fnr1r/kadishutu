from dataclasses import dataclass
from uuid import UUID

from typing_extensions import Self


UE_SAVEGAME_FILE_TYPE_TAG = b"SAVG"
UE_SAVEGAME_FILE_TYPE_TAG_INT = int.from_bytes(UE_SAVEGAME_FILE_TYPE_TAG, "big")


@dataclass
class FEngineVersion:
    major: int
    minor: int
    patch: int
    change_list: int
    branch: str

    def __str__(self) -> str:
        return "{}.{}.{}-{}{}".format(
            self.major,
            self.minor,
            self.patch,
            self.change_list,
            self.branch[1:],
        )


@dataclass
class FCustomVersion:
    key: UUID
    version: int

    @classmethod
    def from_bytearray(cls, data: bytearray) -> Self:
        return cls(
            UUID(bytes=bytes(data[:0x10])),
            int.from_bytes(data[0x10:], "little")
        )


def extract_fstring(data: bytearray, offset: int, size: int) -> str:
    wide = False
    char_size = 1
    if size < 0:
        wide = True
    text_data = data[offset:offset + size * char_size]
    assert text_data[-1] == 0
    if wide:
        text = text_data.decode("UTF-16")
    else:
        text = text_data.decode()
    return text
