from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from pathlib import Path
from typing import List, Optional, Self

from .csvutils import TABLES_PATH, make_maps


MIRACLE_DATA_PATH = TABLES_PATH / "miracles.json"


MIRACLE_TABLE_OFFSET = 0x3d4e


@dataclass
class Miracle(DataClassJsonMixin):
    id: int = field(
        metadata=config(
            decoder=lambda u: int(u, 16),
            encoder=lambda t: f"0x{t:x}"
        )
    )
    name: str
    desc: Optional[str] = None

    @property
    def offset(self) -> int:
        return MIRACLE_TABLE_OFFSET + self.id

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


@dataclass
class MiracleUnlock:
    id: int
    name: str
    miracles: List[Miracle]


MIRACLE_DATA = Miracle.load_path(MIRACLE_DATA_PATH)


(MIRACLE_ID_MAP, MIRACLE_NAME_MAP) = make_maps(MIRACLE_DATA)


MIRACLE_UNLOCK_OFFSET_DATA = [
    *range(0x67a3, 0x67a9),
    *range(0x67b7, 0x67bc),
    *range(0x67df, 0x67e5),
    *range(0x67e8, 0x67ef),
]


MIRACLE_UNLOCK_DATA: List[MiracleUnlock] = [
    MiracleUnlock(i, f"Unnamed 0x{i:04x}", [])
    for i in MIRACLE_UNLOCK_OFFSET_DATA
]


for id, mir in [
    (0x67f3, "Inheritance Violation"),
    (0x67f4, "Rank Violation"),
    (0x67f5, "Moral Transcendence"),
]:
    MIRACLE_UNLOCK_DATA.append(MiracleUnlock(
        id, f"Special: {mir}", [MIRACLE_NAME_MAP[mir]]
    ))
