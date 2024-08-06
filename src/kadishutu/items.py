from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Dict, List, Optional

from .data.items import BUILTIN_ITEM_TABLE, ITEM_TABLE_OFFSET
from .file_handling import BaseDynamicEditor, BaseStaticEditor, BaseStructAsSingularValueEditor


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


class Item(BaseDynamicEditor, BaseStructAsSingularValueEditor):
    struct = "<B"

    @property
    def item_info(self) -> ItemInfo:
        return [
            i
            for i in ITEM_TABLE.items
            if i.offset == self.offset
        ][0]

    @property
    def name_table(self) -> Dict[int, str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.item_info.name

    amount = property(lambda x: x.value, lambda x, y: x.struct_pack(0, y))

    @property
    def limit(self) -> int:
        return self.item_info.get_limit()


class ItemManager(BaseStaticEditor):
    offset = 0x4c72

    def at_offset(self, offset: int) -> Item:
        return self.dispatch(Item, offset)

    def from_name(self, name: str) -> Item:
        return self.at_offset([
            i
            for i in ITEM_TABLE.items
            if i.name == name
        ][0].offset)
