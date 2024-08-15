from typing import Dict, Optional

from .data.items import ITEM_ID_MAP, ITEM_NAME_MAP, ITEM_TABLE_OFFSET, Item
from .file_handling import BaseDynamicEditor, BaseStaticEditor, BaseStructAsSingularValueEditor


class ItemEditor(BaseDynamicEditor, BaseStructAsSingularValueEditor):
    struct = "<B"

    def __init__(self, *args, meta: Optional[Item] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta

    @property
    def meta(self) -> Item:
        if not self._meta:
            self._meta = ITEM_ID_MAP[self.offset - ITEM_TABLE_OFFSET]
        return self._meta

    @property
    def name_table(self) -> Dict[int, str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.meta.name

    amount = property(lambda x: x.value, lambda x, y: x.struct_pack(0, y))

    @property
    def limit(self) -> int:
        return self.meta.limit


class ItemManager(BaseStaticEditor):
    offset = 0x4c72
    SUBEDITOR = ItemEditor

    def at_offset(self, offset: int, *args, **kwargs):
        return self.dispatch(self.SUBEDITOR, offset, *args, **kwargs)

    def from_meta(self, item: Item):
        return self.at_offset(item.offset, meta=item)

    def from_name(self, name: str):
        return self.from_meta(ITEM_NAME_MAP[name])
