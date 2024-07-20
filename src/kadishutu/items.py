from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Dict, List, Optional

from .data.items import BUILTIN_ITEM_TABLE, ITEM_TABLE_OFFSET
from .file_handling import BaseEditor, SingularIntEditor


@dataclass
class ItemInfo(DataClassJsonMixin):
    id: int
    name: str
    desc: Optional[str] = None
    limit: Optional[int] = None

    def get_limit(self) -> int:
        if self.limit:
            return self.limit
        return 99

    @property
    def offset(self) -> int:
        return ITEM_TABLE_OFFSET + self.id


@dataclass
class ItemTable(DataClassJsonMixin):
    items: List[ItemInfo]


ITEM_TABLE = ItemTable.from_dict({"items": BUILTIN_ITEM_TABLE})


class Item(SingularIntEditor):
    fmt = "<B"

    @property
    def name_table(self) -> Dict[int, str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return [
            i
            for i in ITEM_TABLE.items
            if i.offset == self.offset
        ][0].name

    amount = property(lambda x: x.get(), lambda x, y: x.set(y))


class ItemManager(BaseEditor):
    def at_offset(self, offset: int) -> Item:
        return Item(self.saveobj, offset)
    def from_name(self, name: str) -> Item:
        return Item(self.saveobj, [
            i
            for i in ITEM_TABLE.items
            if i.name == name
        ][0].offset)
