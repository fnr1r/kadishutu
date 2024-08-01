from dataclasses import dataclass
import os
from pathlib import Path

from .csvutils import PandasMixin, is_unused, make_maps


file_path = Path(os.path.realpath(__file__)).parent


aaa = file_path / "tables"
action_skills = aaa / "SMT5V Skill Data Tables - ActionSkills.csv"
auto_skills = aaa / "SMT5V Skill Data Tables - AutoSkills.csv"


@dataclass
class Skill(PandasMixin):
    name: str
    id: int


ACTION_SKILLS = Skill.from_csv(
    action_skills,
    rename={"Skill Name": "name", "Skill ID": "id"},
    skiprows=3,
)
AUTO_SKILLS = Skill.from_csv(
    auto_skills,
    rename={"Name": "name", "Skill ID": "id"},
    skiprows=1,
)


NEW_SKILLS = [
    skill
    for skill in (ACTION_SKILLS + AUTO_SKILLS)
    if not is_unused(skill.name)
]

NEW_SKILLS.sort(key=lambda x: x.id)


(SKILL_ID_MAP, SKILL_NAME_MAP) = make_maps(NEW_SKILLS)
