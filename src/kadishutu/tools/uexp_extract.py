from dataclasses import dataclass
from pathlib import Path
import re
from typing import BinaryIO, Dict, List

from typing_extensions import Self

from .extio import ExtIO


UEXP_ENTRIES_OFFSET = 0x20
UEXP_ENTRIES_FMT = "<H"


ID_REGEXP = r"[0-9A-Z]{32}"
NULLTERM_STR = r"(?!\s*$).+"


def re_combine() -> str:
    return "".join([
        "!\0\0\0",
        ID_REGEXP,
    ])


@dataclass
class UExpOffsets:
    offset: int

    @property
    def id(self) -> int:
        return self.offset + 4

    @property
    def length(self) -> int:
        return self.id + 32
    
    @property
    def text(self) -> int:
        return self.length + 1 + 4


@dataclass
class UExpTranslationFile:
    ids: List[str]
    textl: List[str]
    textmap: Dict[str, str]

    @classmethod
    def _open(cls, file: ExtIO) -> Self:
        matches = re.finditer(
            re_combine().encode("ascii"),
            file.read(),
        )
        ids = []
        textl = []
        res = {}
        for i in matches:
            offsets = UExpOffsets(i.span()[0])
            file.seek(offsets.id)
            txt_id = file.read_chars(32, "ascii")
            #file.seek(offsets.length)
            #strlen = file.read_u16_be()
            #if strlen == 0:
            #    print(i, "strlen is 0")
            #    continue
            file.seek(offsets.text)
            data = file.read(2)
            encs = [file.read_utf16_le_until_null, file.read_until_null]
            if data[1] != 0:
                encs.reverse()
            txt = ""
            for enc_fun in encs:
                file.seek(offsets.text)
                try:
                    txt = enc_fun()
                except UnicodeDecodeError:
                    continue
                else:
                    break
            #act_len = len(txt) + 1
            #if strlen != act_len:
            #    print("Meta for", i)
            #    print(txt_id, strlen)
            #    print(strlen, "!=", act_len)
            ids.append(txt_id)
            textl.append(txt)
            res[txt_id] = txt
        return cls(ids, textl, res)

    @classmethod
    def open(cls, file: BinaryIO) -> Self:
        return cls._open(ExtIO.from_parent(file))

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls.open(path.open("rb"))
