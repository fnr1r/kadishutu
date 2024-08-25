from kadishutu.data.miracle_unlocks import (
    MIRACLE_UNLOCK_NAME_MAP, MiracleUnlock,
)
from typing import Optional

from ..shared.file_handling import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructAsSingularValueEditor,
    BitEditor,
)


class MiracleUnlockEditor(BaseDynamicEditor, BaseStructAsSingularValueEditor):
    struct = "<B"
    _meta: Optional[MiracleUnlock] = None

    def __init__(self, *args, meta: Optional[MiracleUnlock] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta

    @property
    def meta(self) -> MiracleUnlock:
        if not self._meta:
            raise NotImplementedError
        return self._meta

    @property
    def state(self) -> bool:
        return bool(self.value)

    @state.setter
    def state(self, value: bool):
        self.value = int(value)


class ExtraMiracleUnlock(BaseStaticEditor):
    offset = 0
    satan_beaten = BitEditor(0x69ce4, 4)


class MiracleUnlockManager(BaseStaticEditor):
    offset = 0

    @property
    def extras(self) -> ExtraMiracleUnlock:
        return self.dispatch(ExtraMiracleUnlock)

    def at_offset(self, offset: int, *args, **kwargs):
        return self.dispatch(MiracleUnlockEditor, offset, *args, **kwargs)

    def from_meta(self, meta: MiracleUnlock):
        return self.at_offset(meta.id, meta=meta)

    def from_name(self, name: str):
        return self.from_meta(MIRACLE_UNLOCK_NAME_MAP[name])
