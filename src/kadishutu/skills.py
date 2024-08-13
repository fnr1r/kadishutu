from typing import Tuple, Union

from .data.skills import SKILL_ID_MAP
from .file_handling import BaseDynamicEditor, BaseStructAsFieldEditor, structproperty


class SkillEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<I"

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
