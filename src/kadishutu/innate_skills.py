from typing import Dict

from .data.innate_skills import INNATE_SKILLS
from .file_handling import SingularIntEditor


def get_innate_skill_name(iskill: int) -> str:
    return INNATE_SKILLS[iskill]


class InnateSkillEditor(SingularIntEditor):
    fmt = "<H"

    @property
    def name_table(self) -> Dict[int, str]:
        return INNATE_SKILLS

    id = property(lambda x: x.get(), lambda x, y: x.set(y))
