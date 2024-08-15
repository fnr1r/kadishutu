from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from typing_extensions import Self

from .affinity import Affinity
from .demon_race import DemonRace
from .old_demon_data import DEMONS_OLD
from .skills import SKILL_ID_MAP, Skill
from .csvutils import TABLES_PATH, FromCsv, extract_from_str, is_unused, make_maps, reverse_extractor


DEMON_DATA_PATH = TABLES_PATH / "SMT5V NKM Base Table_Navi Devil Data - Players.csv"


@dataclass
class LearnedSkill:
    skill: Skill
    level: int


def d_to_skills(data: Dict[str, str]) -> List[Skill]:
    skills = []
    for i in range(12):
        i += 1
        skill_k = f"Skill {i}"
        skill_txt = data[skill_k]
        if not skill_txt:
            continue
        (_, skill_id) = reverse_extractor(skill_txt)
        skill = SKILL_ID_MAP[skill_id]
        skills.append(skill)
    return []


def d_to_learned_skills(data: Dict[str, str]) -> List[LearnedSkill]:
    learned_skills = []
    for i in range(12):
        i += 1
        skill_level_k = f"Skill Level {i}"
        skill_at_level_k = f"Skill at Skill Level {i}"
        try:
            skill_level = int(data[skill_level_k])
        except ValueError:
            continue
        skill_id = int(data[skill_at_level_k])
        learned_skill = LearnedSkill(
            SKILL_ID_MAP[skill_id], skill_level
        )
        learned_skills.append(learned_skill)
    return learned_skills


def d_to_innate_skill(data: Dict[str, str]) -> Skill:
    innate_skill_txt = data["Innate Skill"]
    (_, skill_id) = reverse_extractor(innate_skill_txt)
    return SKILL_ID_MAP[skill_id]


@dataclass
class DemonAffinities:
    physical: Affinity
    fire: Affinity
    ice: Affinity
    electric: Affinity
    force: Affinity
    light: Affinity
    dark: Affinity
    almighty: Affinity
    poison: Affinity
    vertigo: Affinity
    confusion: Affinity

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Self:
        NAMES = [
            "Phys", "Fire", "Ice", "Elec", "Force", "Light", "Dark",
            "Almighty", "Poison", "Vertigo", "Confusion", "Charm", "Sleep",
            "Seal", "Stray", "Burn", "Freeze", "Shock", "Laceration", "Stone",
            "Mirage", "Mud"
        ]
        affinityv = [
            data[i]
            for i in NAMES
        ]
        extracted = []
        for i in affinityv:
            try:
                v = int(i)
            except:
                v = reverse_extractor(i)[1]
            extracted.append(v)
        aff = [
            Affinity(i)
            for i in extracted
        ]
        return cls(*aff[:len(cls.__annotations__)])


@dataclass
class DemonDataTab(FromCsv):
    id: int
    name_id: int
    name: str
    race: DemonRace
    skills: List[Skill]
    learned_skills: List[LearnedSkill]
    innate_skill: Skill
    affinities: DemonAffinities

    @classmethod
    def filter_data(cls, item: Dict[str, str]) -> bool:
        return not (is_unused(item["Name"]) or (item["Name"] == "Jack Frost" and item["ID"] != "58"))

    @classmethod
    def converter_data(cls):
        return {
            "id": {
                "field_name": "ID",
            },
            "name": {
                "field_name": "Name",
            },
            "name_id": {
                "field_name": "Name ID",
            },
            "race": {
                "field_name": "Race",
                "converter": extract_from_str,
            },
            "skills": {
                "eval": d_to_skills,
            },
            "learned_skills": {
                "eval": d_to_learned_skills,
            },
            "innate_skill": {
                "eval": d_to_innate_skill,
            },
            "affinities": {
                "eval": DemonAffinities.from_data,
            },
        }


NEW_DEMONS = DemonDataTab.from_csv(DEMON_DATA_PATH, 1)


@dataclass
class OldDemonData:
    id: int
    name: Optional[str]
    lore: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        try:
            name = data["name"]
        except KeyError:
            name = None
        try:
            lore = data["lore"]
        except KeyError:
            lore = None
        return cls(data["id"], name, lore)


DEMONS_OLD_PARSED = [
    OldDemonData.from_dict(i)
    for i in DEMONS_OLD
]


@dataclass
class Demon:
    id: int
    name: str
    lore: Optional[str] = None

    @classmethod
    def from_new(cls, demon: DemonDataTab) -> Self:
        return cls(demon.id, demon.name)

    def override(self, demon: OldDemonData):
        if demon.name:
            self.name = demon.name
        self.lore = demon.lore
        # Conflict check
        for other in DEMONS:
            if other == self:
                continue
            if other.name != self.name:
                continue
            other.name = f"{other.name} ({other.id})"


DEMONS = [
    Demon.from_new(i)
    for i in NEW_DEMONS
]


for i in DEMONS_OLD_PARSED:
    try:
        demon = [
            j
            for j in DEMONS
            if j.id == i.id
        ][0]
    except IndexError:
        continue
    demon.override(i)


(DEMON_ID_MAP, DEMON_NAME_MAP) = make_maps(DEMONS)
