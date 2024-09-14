from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from typing_extensions import Self

from .tools.dataclasses_json import bytes_config, hex_int_config
from .tools.path import TABLES_PATH


LAYLINE_DATA_PATH = TABLES_PATH / "laylines.json"


LAYLINE_UNLOCK_OFFSET = 0x80a2


@dataclass
class LaylineUnlock(DataClassJsonMixin):
    offset: int = field(
        metadata=hex_int_config(5)
    )
    bit: int


@dataclass
class Layline(DataClassJsonMixin):
    id: int = field(
        metadata=hex_int_config(0)
    )
    name: str
    map_upper: int = field(
        metadata=hex_int_config(8)
    )
    map_lower: int = field(
        metadata=hex_int_config(8)
    )
    coordinates: bytes = field(
        metadata=bytes_config(12)
    )
    rotation: bytes = field(
        metadata=bytes_config(8)
    )
    unlock: Optional[LaylineUnlock] = None

    @staticmethod
    def unlock_data_from_id(id: int) -> Tuple[int, int]:
        (offset, bit) = divmod(id, 8)
        offset += LAYLINE_UNLOCK_OFFSET
        return (offset, bit)

    @property
    def unlock_data(self) -> Tuple[int, int]:
        return self.unlock_data_from_id(self.id)

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


LAYLINE_DATA = Layline.load_path(LAYLINE_DATA_PATH)


## Converter sanity check
#for layline in LAYLINE_DATA:
#    if not layline.unlock:
#        continue
#    assert layline.unlock.offset == layline.unlock_data[0]
#    assert layline.unlock.bit == layline.unlock_data[1]


def make_alignment_map() -> Tuple[Dict[int, Layline], Dict[str, Layline]]:
    id_map = {}
    name_map = {}
    for layline in LAYLINE_DATA:
        id_map[layline.id] = layline
        name_map[layline.name] = layline
    return (id_map, name_map)


(LAYLINE_ID_MAP, LAYLINE_NAME_MAP) = make_alignment_map()
