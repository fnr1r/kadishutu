from typing import Tuple, Union

from .data.skills import SKILLS
from .file_handling import BaseStructFieldEditor, structproperty


def get_skill_name(skill: int) -> str:
    return SKILLS[skill]


class Skill(BaseStructFieldEditor):
    FIELD_FMT = "<L"

    @structproperty(int, FIELD_FMT)
    def _unknown(self):
        return self.relative_field_offset(0)

    @structproperty(int, FIELD_FMT)
    def id(self):
        return self.relative_field_offset(1)
    
    @property
    def name(self) -> str:
        return SKILLS[self.id]


class SkillEditor(BaseStructFieldEditor):
    FIELD_FMT = "<LL"

    def slot(self, no: int) -> Skill:
        return Skill(self.saveobj, self.relative_field_offset(no))

    def __getitem__(self, indices: Union[int, Tuple[int, ...]]) -> Skill:
        if isinstance(indices, tuple):
            raise NotImplemented
        return self.slot(indices)
