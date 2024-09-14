from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from .element_icons import Element
from .tools.csv import FromCsv, extract_from_str
from .tools.mapping import make_maps
from .tools.path import TABLES_PATH
from .tools.unused import is_unused


ACTION_SKILLS_PATH = TABLES_PATH / "SMT5V Skill Data Tables - ActionSkills.csv"
AUTO_SKILLS_PATH = TABLES_PATH / "SMT5V Skill Data Tables - AutoSkills.csv"


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
class ActionSkill(FromCsv):
    name: str
    id: int
    mp_cost: int
    #skill_type: str
    #skill_attribute_1: str
    #magatsuhi: Optional[str]
    icon: Element

    @classmethod
    def converter_data(cls):
        return {
            "name": {
                "field_name": "Skill Name",
            },
            "id": {
                "field_name": "Skill ID",
            },
            "mp_cost": {
                "field_name": "MP Cost",
            },
            #"Skill Type": "skill_type",
            #"Skill Attribute 1": "skill_attribute_1",
            #"Magatsuhi": "magatsuhi",
            "icon": {
                "field_name": "Skill Icon",
                "converter": extract_from_str,
            },
        }


ACTION_SKILLS = ActionSkill.from_csv(ACTION_SKILLS_PATH, 3)


@dataclass
class AutoSkill(FromCsv):
    name: str
    id: int

    @classmethod
    def converter_data(cls) -> Dict[str, Dict[str, Any]] | None:
        return {
            "name": {
                "field_name": "Name",
            },
            "id": {
                "field_name": "Skill ID",
            },
        }


AUTO_SKILLS = AutoSkill.from_csv(AUTO_SKILLS_PATH, 1)


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
        skill.name, skill.id, skill.mp_cost, skill.icon
    ))


for skill in AUTO_SKILLS:
    if is_unused(skill.name):
        continue
    NEW_SKILLS.append(Skill(
        skill.name, skill.id, 0, Element.Passive
    ))


NEW_SKILLS.sort(key=lambda x: x.id)


(SKILL_ID_MAP, SKILL_NAME_MAP) = make_maps(NEW_SKILLS)
