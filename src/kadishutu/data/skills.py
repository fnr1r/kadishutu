from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
import re
from typing import List, Tuple

from .csvutils import PandasMixin, is_unused, make_maps
from .element_icons import Element


file_path = Path(os.path.realpath(__file__)).parent


aaa = file_path / "tables"
action_skills = aaa / "SMT5V Skill Data Tables - ActionSkills.csv"
auto_skills = aaa / "SMT5V Skill Data Tables - AutoSkills.csv"


EXTRACTOR_RE = re.compile(r"(\d+) \((.+)\)")


def extractor(text: str) -> Tuple[int, str]:
    res = EXTRACTOR_RE.match(text)
    assert res
    g = res.groups()
    return (int(g[0]), g[1])


def sktp(cls, text: str):
    (num, _) = extractor(text)
    return cls(num)


class SkillType(Enum):
    E_SKILL_TYPE_PHYSICAL_ATK = 0
    E_SKILL_TYPE_MAGIC_ATK = 1
    E_SKILL_TYPE_NODAMAGE_ATK = 2
    E_SKILL_TYPE_RECOVERY = 3
    E_SKILL_TYPE_AID = 4
    E_SKILL_TYPE_SUMMON = 7
    E_SKILL_TYPE_SPECIAL_ATK = 8
    E_SKILL_TYPE_CALL = 9
    E_SKILL_TYPE_EXTRA_ATK = 13
    E_SKILL_TYPE_PHYSICAL_RATE_ATK = 14


class SkillAttribute1(Enum):
    Physical = 0
    Fire = 1
    Ice = 2
    Electric = 3
    Force = 4
    Light = 5
    Dark = 6
    Almighty = 7
    Poison = 8
    Confusion = 10
    Charm = 11
    Sleep = 12
    Seal = 13
    Mirage = 20
    Invalid = 32


class Magatsuhi(Enum):
    # Or empty for not
    Player = 1
    Enemy = 0


@dataclass
class ActionSkill(PandasMixin):
    name: str
    id: int
    mp_cost: int
    #skill_type: str
    #skill_attribute_1: str
    #magatsuhi: Optional[str]
    icon: str

    @property
    def element(self) -> Element:
        #print(type(self.magatsuhi), self.magatsuhi)
        #skill_type = sktp(SkillType, self.skill_type)
        #skill_attribute_1 = sktp(SkillAttribute1, self.skill_type)
        #if skill_type == SkillType.E_SKILL_TYPE_PHYSICAL_ATK:
        #    return SKILL_ATTR_1_MAP[skill_attribute_1]
        #if skill_type == SkillType.E_SKILL_TYPE_MAGIC_ATK:
        #    return SKILL_ATTR_1_MAP[skill_attribute_1]
        #if skill_type == SkillType.E_SKILL_TYPE_NODAMAGE_ATK:
        #    return SKILL_ATTR_1_MAP[skill_attribute_1]
        #if skill_type == SkillType.E_SKILL_TYPE_RECOVERY:
        #    return Element.Recovery
        #if skill_type == SkillType.E_SKILL_TYPE_SUMMON:
        #    return Element.Support
        #return Element.Misc
        (num, _) = extractor(self.icon)
        return Element(num)


ACTION_SKILLS = ActionSkill.from_csv(
    action_skills,
    rename={
        "Skill Name": "name",
        "Skill ID": "id",
        "MP Cost": "mp_cost",
        #"Skill Type": "skill_type",
        #"Skill Attribute 1": "skill_attribute_1",
        #"Magatsuhi": "magatsuhi",
        "Skill Icon": "icon",
    },
    skiprows=3,
)


@dataclass
class AutoSkill(PandasMixin):
    name: str
    id: int


AUTO_SKILLS = AutoSkill.from_csv(
    auto_skills,
    rename={"Name": "name", "Skill ID": "id"},
    skiprows=1,
)


@dataclass
class Skill:
    name: str
    id: int
    mp_cost: int
    icon: Element


NEW_SKILLS: List[Skill] = []


for skill in ACTION_SKILLS:
    if is_unused(skill.name):
        continue
    NEW_SKILLS.append(Skill(
        skill.name, skill.id, skill.mp_cost, skill.element
    ))


for skill in AUTO_SKILLS:
    if is_unused(skill.name):
        continue
    NEW_SKILLS.append(Skill(
        skill.name, skill.id, 0, Element.Passive
    ))


NEW_SKILLS.sort(key=lambda x: x.id)


(SKILL_ID_MAP, SKILL_NAME_MAP) = make_maps(NEW_SKILLS)
