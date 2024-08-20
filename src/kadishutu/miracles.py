from enum import IntFlag, auto
from typing import Optional

from .data.miracles import MIRACLE_ID_MAP, MIRACLE_NAME_MAP, MIRACLE_TABLE_OFFSET, Miracle
from .file_handling import BaseDynamicEditor, BaseStaticEditor, BaseStructAsSingularValueEditor


class MiracleState(IntFlag):
    Bought = auto()
    Seen = auto()
    Enabled = auto()

    @classmethod
    def none(cls):
        return cls(0)

    @classmethod
    def all(cls):
        return cls(7)


class MiracleEditor(BaseDynamicEditor, BaseStructAsSingularValueEditor):
    struct = "<B"
    _meta: Optional[Miracle] = None

    def __init__(self, *args, meta: Optional[Miracle] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta

    @property
    def meta(self) -> Miracle:
        if not self._meta:
            self._meta = MIRACLE_ID_MAP[self.offset]
        return self._meta

    @property
    def state(self) -> MiracleState:
        return MiracleState(self.value)

    @state.setter
    def state(self, value: MiracleState):
        self.value = value.value

    @property
    def name(self) -> str:
        return self.meta.name


class MiracleManager(BaseStaticEditor):
    offset = 0

    def at_offset(self, offset: int, *args, **kwargs):
        return self.dispatch(MiracleEditor, offset, *args, **kwargs)

    def from_id(self, id: int):
        return self.at_offset(MIRACLE_TABLE_OFFSET + id)

    def from_meta(self, meta: Miracle):
        return self.at_offset(meta.offset, meta=meta)

    def from_name(self, name: str):
        return self.from_meta(MIRACLE_NAME_MAP[name])
