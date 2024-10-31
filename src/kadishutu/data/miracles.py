from dataclasses import dataclass, field
from enum import Enum
from struct import Struct
from pathlib import Path
from typing import List, Optional, Union

from dataclasses_json import DataClassJsonMixin
from typing_extensions import Self

from kadishutu.paths import APPDIRS
from kadishutu.tools.eprint import printexcept
from kadishutu.tools.tbbreader import Tbcr

from .tools.dataclasses_json import hex_int_config
from .tools.mapping import make_maps
from .tools.path import TABLES_PATH
from .tools.unused import is_unused


UMODEL_SAVED_PATH = APPDIRS.data_path / "game_data_saved"
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
    tcx = Tbcr.from_path(UMODEL_SAVED_PATH / "Game/Blueprints/Gamedata/BinTable/GodParameter/Table/GodParameterDataTable.uexp")
    MIRACLE_DATA = MiracleData.from_array_of_bytes(tcx.tables[0].rows)
except Exception as e:
    printexcept("Failed to load miracle data", e)
    MIRACLE_DATA = []


@dataclass
class MiracleText(DataClassJsonMixin):
    id: int = field(
        metadata=hex_int_config(2)
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
