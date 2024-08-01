from typing import Tuple, Union

from .data.skills import SKILL_ID_MAP
from .file_handling import BaseStructFieldEditor, structproperty


class Skill(BaseStructFieldEditor):
    FIELD_FMT = "<I"

    @structproperty(int, FIELD_FMT)
    def _unknown(self):
        return self.relative_field_offset(0)

    @structproperty(int, FIELD_FMT)
    def id(self):
        return self.relative_field_offset(1)

    @property
    def name(self) -> str:
        return SKILL_ID_MAP[self.id].name


class SkillEditor(BaseStructFieldEditor):
    FIELD_FMT = "<II"

    def slot(self, no: int) -> Skill:
        return Skill(self.saveobj, self.relative_field_offset(no))

    def __getitem__(self, indices: Union[int, Tuple[int, ...]]) -> Skill:
        if isinstance(indices, tuple):
            raise NotImplementedError
        return self.slot(indices)
