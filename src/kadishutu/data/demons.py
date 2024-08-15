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
class DemonStats:
    hp: int
    mp: int
    strength: int
    vitality: int
    magic: int
    agility: int
    luck: int

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Self:
        NAMES = [
            "HP", "MP", "Strength", "Vitality", "Magic", "Agility", "Luck",
        ]
        stats = [
            int(data[i])
            for i in NAMES
        ]
        return cls(*stats)


@dataclass
class LearnedSkill:
    skill: Skill
    level: int

    @classmethod
    def from_data(cls, data: Dict[str, str], i: int) -> Optional[Self]:
        skill_level_k = f"Skill Level {i}"
        skill_at_level_k = f"Skill at Skill Level {i}"
        try:
            skill_level = int(data[skill_level_k])
        except ValueError:
            return None
        skill_id = int(data[skill_at_level_k])
        learned_skill = cls(
            SKILL_ID_MAP[skill_id], skill_level
        )
        return learned_skill

    @classmethod
    def list_from_data(cls, data: Dict[str, str]) -> List[Self]:
        learned_skills = [
            cls.from_data(data, i + 1)
            for i in range(12)
        ]
        return [
            i
            for i in learned_skills
            if i is not None
        ]


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
    _: Affinity
    confusion: Affinity
    charm: Affinity
    sleep: Affinity
    seal: Affinity
    _: Affinity
    _: Affinity
    _: Affinity
    _: Affinity
    _: Affinity
    _: Affinity
    mirage: Affinity

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
            except ValueError:
                v = reverse_extractor(i)[1]
            extracted.append(v)
        aff = [
            Affinity(i)
            for i in extracted
        ]
        return cls(*aff[:len(cls.__annotations__)])


@dataclass
class DemonPotentials:
    physical: int
    fire: int
    ice: int
    electric: int
    force: int
    light: int
    dark: int
    almighty: int
    ailment: int
    support: int
    recovery: int

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Self:
        NAMES = [
            "PotPhys", "PotFire", "PotIce", "PotElec", "PotForce", "PotLight",
            "PotDark", "PotAlmighty", "PotAilment", "PotSupport", "PotHeal",
        ]
        stats = [
            int(data[i])
            for i in NAMES
        ]
        return cls(*stats)


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
    return skills


def d_to_innate_skill(data: Dict[str, str]) -> Skill:
    innate_skill_txt = data["Innate Skill"]
    (_, skill_id) = reverse_extractor(innate_skill_txt)
    return SKILL_ID_MAP[skill_id]


@dataclass
class DemonDataTab(FromCsv):
    id: int
    name_id: int
    name: str
    race: DemonRace
    level: int
    stats: DemonStats
    skills: List[Skill]
    learned_skills: List[LearnedSkill]
    innate_skill: Skill
    affinities: DemonAffinities
    potentials: DemonPotentials

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
            "level": {
                "field_name": "Level",
            },
            "stats": {
                "eval": DemonStats.from_data,
            },
            "skills": {
                "eval": d_to_skills,
            },
            "learned_skills": {
                "eval": LearnedSkill.list_from_data,
            },
            "innate_skill": {
                "eval": d_to_innate_skill,
            },
            "affinities": {
                "eval": DemonAffinities.from_data,
            },
            "potentials": {
                "eval": DemonPotentials.from_data,
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
    level: int
    stats: DemonStats
    skills: List[Skill]
    innate_skill: Skill
    affinities: DemonAffinities
    potentials: DemonPotentials
    lore: Optional[str] = None

    @classmethod
    def from_new(cls, demon: DemonDataTab) -> Self:
        return cls(
            demon.id, demon.name,
            demon.level,
            demon.stats,
            demon.skills,
            demon.innate_skill,
            demon.affinities,
            demon.potentials,
        )

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
