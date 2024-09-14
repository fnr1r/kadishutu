from enum import IntFlag, auto
from kadishutu.core.shared.editors import BoolEditor, EnumEditor
from kadishutu.data.items import ESSENCES_RANGE, ITEM_TABLE_OFFSET, Item

from .items import ItemEditor, ItemManager


class EssenceMetadata(IntFlag):
    Bit0 = auto()
    New = auto()
    Owned = auto()
    Bit3 = auto()
    Absent = auto()
    Bit5 = auto()
    Bit6 = auto()
    Bit7 = auto()

    @classmethod
    def all(cls):
        return cls(0xff)

    @classmethod
    def new_blockbits(cls):
        return [EssenceMetadata.Owned, EssenceMetadata.Absent]


class EssenceEditor(ItemEditor):
    owned = BoolEditor(0)
    metadata = EnumEditor(0x380, EssenceMetadata)

    def is_absent(self) -> bool:
        return False

    def is_owned(self) -> bool:
        return False

    def add_bits(self, bits: EssenceMetadata):
        self.metadata |= bits

    def remove_bits(self, bits: EssenceMetadata):
        self.metadata &= ~bits

    def is_new(self) -> bool:
        for i in EssenceMetadata.new_blockbits():
            if self.metadata & i:
                return False
        return bool(self.metadata & EssenceMetadata.New)

    def give(self, new: bool = False):
        self.add_bits(EssenceMetadata.New)
        if new:
            self.remove_bits(EssenceMetadata.Owned)
        else:
            self.add_bits(EssenceMetadata.Owned)
        self.remove_bits(EssenceMetadata.Absent)

    def take(self):
        self.add_bits(EssenceMetadata.New)
        self.add_bits(EssenceMetadata.Owned)
        self.add_bits(EssenceMetadata.Absent)


class EssenceManager(ItemManager):
    @staticmethod
    def _return(r: ItemEditor) -> EssenceEditor:
        assert isinstance(r, EssenceEditor)
        return r

    def at_offset(self, offset: int, *args, **kwargs):
        assert offset - ITEM_TABLE_OFFSET in ESSENCES_RANGE
        return self._return(super().at_offset(offset, *args, **kwargs))

    def from_meta(self, item: Item) -> EssenceEditor:
        return self._return(super().from_meta(item))

    def from_name(self, name: str) -> EssenceEditor:
        return self._return(super().from_name(name))
