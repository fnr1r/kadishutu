from dataclasses import dataclass, field
from enum import Enum
from kadishutu.tools.eprint import eprint
from kadishutu.tools.tbbreader import Tbcr
import os
from struct import Struct
from dataclasses_json import DataClassJsonMixin, config
from pathlib import Path
from typing import List, Optional, Self, Union

from .csvutils import TABLES_PATH, is_unused, make_maps


MIRACLE_DATA_PATH = TABLES_PATH / "miracles.json"


MIRACLE_TABLE_OFFSET = 0x3d4e
MIRACLE_NO_NAME = "NOT USED:GP_NAME_{}"


class Destructable:
    def get_format(*args, **kwargs) -> Union[str, bytes]:
        raise NotImplementedError

    @classmethod
    def get_struct(cls, *args, **kwargs) -> Struct:
        return Struct(cls.get_format(*args, **kwargs))

    @classmethod
    def from_bytes(cls, data: bytes, *args, **kwargs) -> Self:
        return cls(*cls.get_struct(*args, **kwargs).unpack(data))

    @classmethod
    def from_array_of_bytes(cls, data: List[bytes], *args, **kwargs) -> List[Self]:
        struct = cls.get_struct(*args, **kwargs)
        return [
            cls(*struct.unpack(i))
            for i in data
        ]


@dataclass
class MiracleData(Destructable):
    id: int
    order_id: int
    category: int
    _pad1: bytes
    cost: int
    toggleable: bool
    _pad2: bytes

    def get_format(*args, **kwargs) -> Union[str, bytes]:
        return "<HIB5sH?5s"


try:
    datadir = Path(os.environ["HOME"]) / ".local/share/kadishutu/game_data_saved"
    tcx = Tbcr.from_path(datadir / "Game/Blueprints/Gamedata/BinTable/GodParameter/Table/GodParameterDataTable.uexp")
    MIRACLE_DATA = MiracleData.from_array_of_bytes(tcx.tables[0].rows)
except Exception as e:
    eprint("Failed to load miracle data:", e.__repr__())
    MIRACLE_DATA = []


@dataclass
class MiracleText(DataClassJsonMixin):
    id: int = field(
        metadata=config(
            decoder=lambda u: int(u, 16),
            encoder=lambda t: f"0x{t:x}"
        )
    )
    name: str
    desc: Optional[str] = None

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


MIRACLE_TEXT_DATA = MiracleText.load_path(MIRACLE_DATA_PATH)


class MiracleCategory(Enum):
    NoCategory = 0
    Supremacy = 1
    Doctrine = 2
    Awakening = 3
    Cosmos = 4


@dataclass
class Miracle:
    id: int
    order_id: Optional[int]
    category: Optional[MiracleCategory]
    cost: Optional[int]
    toggleable: Optional[bool]
    name: str
    desc: Optional[str] = None

    @property
    def offset(self) -> int:
        return MIRACLE_TABLE_OFFSET + self.id

    @classmethod
    def from_data(cls, mir: MiracleData) -> Self:
        return cls(
            mir.id,
            mir.order_id,
            MiracleCategory(mir.category),
            mir.cost,
            mir.toggleable,
            MIRACLE_NO_NAME.format(mir.id),
            None,
        )

    @classmethod
    def from_text(cls, mir: MiracleText) -> Self:
        return cls(
            mir.id,
            None,
            None,
            None,
            None,
            mir.name,
            mir.desc,
        )

    def update_text(self, mir: MiracleText):
        self.name = mir.name
        self.desc = mir.desc


MIRACLES = [
    Miracle.from_data(i)
    for i in MIRACLE_DATA
]


for i in MIRACLE_TEXT_DATA:
    try:
        mir = [
            j
            for j in MIRACLES
            if j.id == i.id
        ][0]
    except IndexError:
        MIRACLES.append(Miracle.from_text(i))
    else:
        mir.update_text(i)


MIRACLES = [
    i
    for i in MIRACLES
    if not is_unused(i.name)
]


MIRACLES.sort(key=lambda x: x.id)


(MIRACLE_ID_MAP, MIRACLE_NAME_MAP) = make_maps(MIRACLES)
