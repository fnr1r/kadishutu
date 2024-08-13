from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from pathlib import Path
from typing import Dict, List, Tuple
from typing_extensions import Self

from .csvutils import TABLES_PATH


LAYLINE_DATA_PATH = TABLES_PATH / "laylines.json"


@dataclass
class Layline(DataClassJsonMixin):
    id: int = field(
        metadata=config(
            decoder=lambda u: int(u, 16),
            encoder=lambda t: f"0x{t:x}"
        )
    )
    name: str
    map_upper: int = field(
        metadata=config(
            decoder=lambda u: int(u, 16),
            encoder=lambda t: f"0x{t:08x}"
        )
    )
    map_lower: int = field(
        metadata=config(
            decoder=lambda u: int(u, 16),
            encoder=lambda t: f"0x{t:04x}"
        )
    )
    coordinates: bytes = field(
        metadata=config(
            decoder=lambda u: bytes.fromhex(u),
            encoder=lambda t: t.hex().rjust(24, "0")
        )
    )
    rotation: bytes = field(
        metadata=config(
            decoder=lambda u: bytes.fromhex(u),
            encoder=lambda t: t.hex().rjust(16, "0")
        )
    )

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


LAYLINE_DATA = Layline.load_path(LAYLINE_DATA_PATH)


def make_alignment_map() -> Tuple[Dict[int, Layline], Dict[str, Layline]]:
    id_map = {}
    name_map = {}
    for layline in LAYLINE_DATA:
        id_map[layline.id] = layline
        name_map[layline.name] = layline
    return (id_map, name_map)


(LAYLINE_ID_MAP, LAYLINE_NAME_MAP) = make_alignment_map()
