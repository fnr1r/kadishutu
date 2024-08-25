from kadishutu.data.skills import SKILL_ID_MAP, Skill
from typing import Optional, Tuple, Union

from ..shared.file_handling import (
    BaseDynamicEditor, BaseStructAsFieldEditor, structproperty,
)


class SkillEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<I"
    _meta: Optional[Skill] = None

    @property
    def meta(self) -> Skill:
        if not self._meta:
            self._meta = SKILL_ID_MAP[self.id]
        return self._meta

    @structproperty(int, struct)
    def _unknown(self):
        return self.field_as_absolute_offset(0)

    @structproperty(int, struct)
    def id(self):
        return self.field_as_absolute_offset(1)

    @property
    def name(self) -> str:
        return SKILL_ID_MAP[self.id].name


class SkillManager(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<II"

    def slot(self, no: int) -> SkillEditor:
        return self.field_dispatch(SkillEditor, no)

    def __getitem__(self, indices: Union[int, Tuple[int, ...]]) -> SkillEditor:
        if isinstance(indices, tuple):
            raise NotImplementedError
        return self.slot(indices)
