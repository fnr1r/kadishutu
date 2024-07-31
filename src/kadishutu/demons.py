from enum import Enum, auto
from struct import calcsize, pack_into, unpack_from

from .data.demons import DEMONS
from .file_handling import BaseIdEditor, BaseEditor, BaseStructFieldEditor, structproperty
from .innate_skills import InnateSkillEditor
from .skills import SkillEditor


def demon_map() -> dict[int, str]:
    res = {}
    for v in DEMONS:
        res[v["id"]] = v["name"]
    return res


DEMON_MAP = demon_map()


def get_demon_name(demon: int) -> str:
    return DEMON_MAP[demon]


DEMON_TABLE_OFFSET = 0xb60
DEMON_ENTRY_SIZE = 424
STAT_TABLE_SIZE = 16


META_STATS = ("<HHHHHHHH", "HP MP ST VI MA AG LU NULL")
META_POTENTIALS = ("<hhhhhhhhhhhh", "PHYSICAL FIRE ICE ELECTRIC FORCE LIGHT DARK ALMIGHTY AILMENT SUPPORT HEALING _unknown")


STATS_NAMES = ["HP", "MP", "Strength", "Vitality", "Magic", "Agility", "Luck"]


class SubStatsEditor(BaseStructFieldEditor):
    FIELD_FMT = "<H"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert not unpack_from(self.FIELD_FMT, self.data, self.relative_field_offset(7))[0],\
            "Supposed NULL is not a null????"

    @structproperty(int, FIELD_FMT)
    def hp(self):
        return self.relative_field_offset(0)

    @structproperty(int, FIELD_FMT)
    def mp(self):
        return self.relative_field_offset(1)

    @structproperty(int, FIELD_FMT)
    def strength(self):
        return self.relative_field_offset(2)

    @structproperty(int, FIELD_FMT)
    def vitality(self):
        return self.relative_field_offset(3)

    @structproperty(int, FIELD_FMT)
    def magic(self):
        return self.relative_field_offset(4)

    @structproperty(int, FIELD_FMT)
    def agility(self):
        return self.relative_field_offset(5)

    @structproperty(int, FIELD_FMT)
    def luck(self):
        return self.relative_field_offset(6)


class StatsEditor(BaseEditor):
    @property
    def base(self) -> SubStatsEditor:
        return self.delegate(SubStatsEditor, 0)
    @property
    def changes(self) -> SubStatsEditor:
        return self.delegate(SubStatsEditor, STAT_TABLE_SIZE * 1)
    @property
    def current(self) -> SubStatsEditor:
        return self.delegate(SubStatsEditor, STAT_TABLE_SIZE * 2)
    def max_with_sbis(self):
        target = 999
        changes = self.changes
        current = self.current
        for stat in ["strength", "vitality", "magic", "agility", "luck"]:
            inc = target - current.__getattribute__(stat)
            print(f"Using {inc} {stat} boosting items.")
            changes.__setattr__(stat, inc)
            current.__setattr__(stat, target)


#class FriendshipEditor(BaseStructEditor):
#    fmt = "<L"
#
#    def get(self) -> int:
#        return self.unpack()[0]
#
#    def set(self, id: int):
#        self.pack(id)


class HealableEditor(BaseStructFieldEditor):
    FIELD_FMT = "<H"
    @structproperty(int, FIELD_FMT)
    def hp(self) -> int:
        return self.relative_field_offset(0)
    @structproperty(int, FIELD_FMT)
    def mp(self) -> int:
        return self.relative_field_offset(1)


#class DemonIdEditor(SingularIntEditor):
#    fmt = "<H"
#
#    @property
#    def name_table(self) -> Dict[int, str]:
#        return DEMONS


class Affinity(Enum):
    Weak = 125
    Neutral = 100
    Resist = 50
    Null = 0
    Repel = 999
    Drain = 1000


class AffinityEditor(BaseStructFieldEditor):
    FIELD_FMT = "<H"
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def physical(self) -> int:
        return self.relative_field_offset(0)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def fire(self) -> int:
        return self.relative_field_offset(1)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def ice(self) -> int:
        return self.relative_field_offset(2)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def electric(self) -> int:
        return self.relative_field_offset(3)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def force(self) -> int:
        return self.relative_field_offset(4)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def light(self) -> int:
        return self.relative_field_offset(5)
    @structproperty(
        Affinity, FIELD_FMT,
        lambda u: Affinity(u),
        lambda t: t.value,
    )
    def dark(self) -> int:
        return self.relative_field_offset(6)


class PType(Enum):
    Physical = 0
    Fire = auto()
    Ice = auto()
    Electric = auto()
    Force = auto()
    Light = auto()
    Dark = auto()
    Almighty = auto()
    Ailment = auto()
    Support = auto()
    Healing = auto()
    _UNKNOWN = auto()


def gsproperty(p: PType):
    return property(
        lambda x: x.get(p),
        lambda x, y: x.set(p, y)
    )


class PotentialEditor(BaseStructFieldEditor):
    FIELD_FMT = "<h"

    def get_offset(self, t: PType) -> int:
        return self.offset + t.value * self.SFMT_LEN

    def get(self, t: PType) -> int:
        return unpack_from(
            self.FIELD_FMT,
            self.data,
            self.get_offset(t)
        )[0]

    def set(self, t: PType, potential: int):
        pack_into(
            self.FIELD_FMT,
            self.data,
            self.get_offset(t),
            potential
        )

    physical = gsproperty(PType.Physical)
    fire = gsproperty(PType.Fire)
    ice = gsproperty(PType.Ice)
    electric = gsproperty(PType.Electric)
    force = gsproperty(PType.Force)
    light = gsproperty(PType.Light)
    dark = gsproperty(PType.Dark)
    almighty = gsproperty(PType.Almighty)
    ailment = gsproperty(PType.Ailment)
    support = gsproperty(PType.Support)
    healing = gsproperty(PType.Healing)


class DemonEditor(BaseIdEditor):
    @classmethod
    def id_to_offset(cls, id: int) -> int:
        return DEMON_TABLE_OFFSET + DEMON_ENTRY_SIZE * id

    @property
    def stats(self) -> StatsEditor:
        return self.delegate(StatsEditor, 0)
    #@property
    #def friendship(self) -> FriendshipEditor:
    #    return self.at_offset(FriendshipEditor, 68)
    @structproperty(int, "<L")
    def friendship(self) -> int:
        return self.relative_offset(68)
    @structproperty(int, "<H") # , lambda u: bool(u), lambda t: int(t)
    def is_summoned(self):
        return self.relative_offset(72)
    @structproperty(int, "<H")
    def dh_talks(self):
        return self.relative_offset(74)
    @property
    def healable(self) -> HealableEditor:
        return self.delegate(HealableEditor, 100)
    @structproperty(int, "<Q")
    def exp(self) -> int:
        return self.relative_offset(104)
    @structproperty(int, "<B")
    def level(self):
        return self.relative_offset(112)
    #@property
    #def demon_id(self) -> DemonIdEditor:
    #    return self.at_offset(DemonIdEditor, 114)
    @structproperty(int, "<H")
    def demon_id(self):
        return self.relative_offset(114)
    @property
    def skills(self) -> SkillEditor:
        return self.delegate(SkillEditor, 120)
    @property
    def affinities(self) -> AffinityEditor:
        return self.delegate(AffinityEditor, 216)
    @property
    def potentials(self) -> PotentialEditor:
        return self.delegate(PotentialEditor, 384)
    @property
    def innate_skill(self) -> InnateSkillEditor:
        return self.delegate(InnateSkillEditor, 408)

    @property
    def name(self) -> str:
        return get_demon_name(self.demon_id)
