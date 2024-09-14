from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import Dict, List, Optional
from typing_extensions import Self

from .tools.dataclasses_json import hex_int_config
from .tools.path import TABLES_PATH


ALIGNMENT_DATA_PATH = TABLES_PATH / "alignment_data.json"


@dataclass
class AlignmentBit(DataClassJsonMixin):
    bit: int
    alignment: str
    place: str
    side_quest: Optional[str]
    text: List[str]


@dataclass
class AlignmentByte(DataClassJsonMixin):
    offset: int = field(
        metadata=hex_int_config(5),
    )
    bits: List[AlignmentBit]

    def __init__(self, offset: int, bits: List[AlignmentBit]):
        self.offset = offset
        self.bits = bits
        self.bitmap = {}
        for bitobj in bits:
            self.bitmap[bitobj.bit] = bitobj

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)

    def has_bit(self, bit: int) -> bool:
        try:
            self.bitmap[bit]
        except IndexError:
            return False
        else:
            return True


ALIGNMENT_DATA = AlignmentByte.load_path(ALIGNMENT_DATA_PATH)


def make_alignment_map() -> Dict[int, AlignmentByte]:
    res = {}
    for byte in ALIGNMENT_DATA:
        res[byte.offset] = byte
    return res


ALIGNMENT_OFFSET_MAP = make_alignment_map()
