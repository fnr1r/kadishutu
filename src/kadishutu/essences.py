from enum import Enum

from .data.items import ESSENCES_RANGE, ITEM_TABLE_OFFSET
from .items import ItemEditor, ItemManager


class EssenceMetadata(Enum):
    NotOwned = 0b00000000
    New = 0b00000010
    Owned2 = 0b00000100
    Owned = 0b00000110
    # An essence can't be new and used
    Used = 0b00010000
    Used2 = 0b00010110


def essence_metadata_map() -> dict[str, EssenceMetadata]:
    res = {}
    for i in EssenceMetadata:
        res[i.name] = i
    return res


ESSENCE_META_MAP = essence_metadata_map()


class EssenceEditor(ItemEditor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def metadata_offset(self) -> int:
        return self.offset + 0x380

    @property
    def name(self) -> str:
        raise NotImplementedError

    owned = property(lambda x: bool(x.amount), lambda x, y: x.set(int(y)))

    @property
    def metadata(self):
        return self.data[self.metadata_offset]
    @metadata.setter
    def metadata(self, value: int):
        self.data[self.metadata_offset] = value

    #def give(self):
    #    if not self.owned:
    #        self.owned = True
    #        self.metadata = EssenceMetadata.New
    #    else:
    #        self.metadata = EssenceMetadata.Owned


class EssenceManager(ItemManager):
    SUBEDITOR = EssenceEditor

    def at_offset(self, offset: int, *args, **kwargs):
        assert offset - ITEM_TABLE_OFFSET in ESSENCES_RANGE
        return super().at_offset(offset, *args, **kwargs)
