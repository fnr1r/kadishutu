from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from pathlib import Path
from typing import List, Optional, Self

from .csvutils import TABLES_PATH, make_maps


MIRACLE_DATA_PATH = TABLES_PATH / "miracles.json"


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
        return self.id

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


MIRACLE_DATA = Miracle.load_path(MIRACLE_DATA_PATH)


(MIRACLE_ID_MAP, MIRACLE_NAME_MAP) = make_maps(MIRACLE_DATA)
