from typing import Dict, Optional

from .data.items import ITEMS, Item
from .file_handling import BaseDynamicEditor, BaseStaticEditor, BaseStructAsSingularValueEditor


class ItemEditor(BaseDynamicEditor, BaseStructAsSingularValueEditor):
    struct = "<B"

    def __init__(self, *args, item_meta: Optional[Item] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._item_meta = item_meta

    @property
    def item_meta(self) -> Item:
        if not self._item_meta:
            self._item_meta = [
                item
                for item in ITEMS
                if item.offset == self.offset
            ][0]
        return self._item_meta

    @property
    def name_table(self) -> Dict[int, str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.item_meta.name

    amount = property(lambda x: x.value, lambda x, y: x.struct_pack(0, y))

    @property
    def limit(self) -> int:
        return self.item_meta.limit


class ItemManager(BaseStaticEditor):
    offset = 0x4c72

    def at_offset(self, offset: int, *args, **kwargs) -> ItemEditor:
        return self.dispatch(ItemEditor, offset, *args, **kwargs)

    def from_name(self, name: str) -> ItemEditor:
        item = [
            item
            for item in ITEMS
            if item.name == name
        ][0]
        return self.at_offset(item.offset, item)
