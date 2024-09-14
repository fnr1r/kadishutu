from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import List, Self

from .miracles import MIRACLE_NAME_MAP, Miracle
from .tools.dataclasses_json import hex_int_config
from .tools.mapping import make_maps
from .tools.path import TABLES_PATH


MIRACLE_UNLOCKS_DATA_PATH = TABLES_PATH / "miracle_unlocks.json"


@dataclass
class MiracleUnlock(DataClassJsonMixin):
    id: int = field(
        metadata=hex_int_config(4)
    )
    name: str
    miracles: List[str]

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)

    @property
    def miracles_obj(self) -> List[Miracle]:
        return [
            MIRACLE_NAME_MAP[i]
            for i in self.miracles
        ]


MIRACLE_UNLOCKS = MiracleUnlock.load_path(MIRACLE_UNLOCKS_DATA_PATH)


(MIRACLE_UNLOCK_ID_MAP, MIRACLE_UNLOCK_NAME_MAP) = make_maps(MIRACLE_UNLOCKS)
