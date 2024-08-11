from dataclasses import dataclass
import os
from pathlib import Path
from typing import List, Optional
from dataclasses_json import DataClassJsonMixin
from pandas import DataFrame, read_csv
from typing_extensions import Self

from .csvutils import is_unused, make_maps


FILE_PATH = Path(os.path.realpath(__file__)).parent

TABLES_PATH = FILE_PATH / "tables"
ITEM_NAMES_TABLE_PATH = TABLES_PATH / "SMT5V NKM Base Table_Navi Devil Data - Item Names.csv"
ITEM_ADDITIONAL_INFO_PATH = TABLES_PATH / "item_extra_data.json"


ITEM_TABLE_OFFSET = 0x4c72

# 0x4c72 - 0
# 0x4c73 - 1
# etc...


TOTAL_ITEM_RANGE = range(0, 895 + 1)
CONSUMABLES_RANGE = range(0, 220 + 1)
ESSENCES_RANGE = range(221, 615 + 1)
RELICS_RANGE_1 = range(616, 655 + 1)
KEY_ITEMS_RANGE = range(656, 855 + 1)
RELICS_RANGE_2 = range(856, 895 + 1)


DEFAULT_LIMIT = 99
ESSENCE_ITEM_LIMIT = 1
RELICS_ITEM_LIMIT = DEFAULT_LIMIT

@dataclass
class AnyItem:
    id: int
    name: str

    @classmethod
    def from_dataframe(cls, df: DataFrame) -> List[Self]:
        return [
            cls(*row.values())
            for row in df.to_dict(orient="records")
        ]
    @classmethod
    def from_csv(cls, path: Path) -> List[Self]:
        with open(path, "r") as file:
            df = read_csv(file, header=None, skiprows=1)
        return cls.from_dataframe(df)


ANY_ITEMS = AnyItem.from_csv(ITEM_NAMES_TABLE_PATH)


@dataclass
class ItemExtraData(DataClassJsonMixin):
    id: int
    limit: Optional[int] = None
    desc: Optional[str] = None

    @classmethod
    def load_path(cls, path: Path) -> List[Self]:
        with open(path, "rt") as file:
            return cls.schema().loads(file.read(), many=True)


ITEM_EXTRA_DATA = ItemExtraData.load_path(ITEM_ADDITIONAL_INFO_PATH)


@dataclass
class Item:
    id: int
    name: str
    _limit: Optional[int]
    desc: Optional[str]

    @property
    def limit(self) -> int:
        if self._limit:
            return self._limit
        elif self.id in ESSENCES_RANGE:
            return ESSENCE_ITEM_LIMIT
        elif self.id in RELICS_RANGE_1 or self.id in RELICS_RANGE_2:
            return RELICS_ITEM_LIMIT
        else:
            return DEFAULT_LIMIT

    @property
    def offset(self) -> int:
        return ITEM_TABLE_OFFSET + self.id

    @classmethod
    def combined(cls) -> List[Self]:
        items = []
        for id in TOTAL_ITEM_RANGE:
            name = [
                it.name
                for it in ANY_ITEMS
                if it.id == id
            ][0]
            if is_unused(name):
                continue
            try:
                extra = [
                    j
                    for j in ITEM_EXTRA_DATA
                    if j.id == id
                ][0]
            except IndexError:
                limit = None
                desc = None
            else:
                limit = extra.limit
                desc = extra.desc
            items.append(cls(id, name, limit, desc))
        return items


ITEMS = Item.combined()


def items_from(*args: range) -> List[Item]:
    return [
        item
        for item in ITEMS
        if any([
            item.id in r
            for r in args
        ])
    ]


def items_except_for(*args: range) -> List[Item]:
    return [
        item
        for item in ITEMS
        if not any([
            item.id in r
            for r in args
        ])
    ]


(ITEM_ID_MAP, ITEM_NAME_MAP) = make_maps(ITEMS)

