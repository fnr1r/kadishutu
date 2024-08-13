from enum import Enum, auto
from struct import calcsize, pack_into, unpack_from

from .data.demons import DEMON_ID_MAP
from .file_handling import BaseDynamicEditor, BaseStructAsFieldEditor, structproperty
from .skills import SkillEditor, SkillManager


DEMON_TABLE_OFFSET = 0xb60
DEMON_ENTRY_SIZE = 424
STAT_TABLE_SIZE = 16


META_STATS = ("<HHHHHHHH", "HP MP ST VI MA AG LU NULL")
META_POTENTIALS = ("<hhhhhhhhhhhh", "PHYSICAL FIRE ICE ELECTRIC FORCE LIGHT DARK ALMIGHTY AILMENT SUPPORT HEALING _unknown")


STATS_NAMES = ["HP", "MP", "Strength", "Vitality", "Magic", "Agility", "Luck"]
AFFINITY_NAMES = [
    "Physical", "Fire", "Ice", "Electric", "Force", "Light", "Dark",
    "Poison", "Confusion", "Charm", "Sleep", "Seal", "Mirage"
]


class SubStatsEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert not self.struct_obj.unpack_from(self.data, self.field_as_absolute_offset(7))[0],\
            "Supposed NULL is not a null????"

    @structproperty(int, struct)
    def hp(self):
        return self.field_as_absolute_offset(0)

    @structproperty(int, struct)
    def mp(self):
        return self.field_as_absolute_offset(1)

    @structproperty(int, struct)
    def strength(self):
        return self.field_as_absolute_offset(2)

    @structproperty(int, struct)
    def vitality(self):
        return self.field_as_absolute_offset(3)

    @structproperty(int, struct)
    def magic(self):
        return self.field_as_absolute_offset(4)

    @structproperty(int, struct)
    def agility(self):
        return self.field_as_absolute_offset(5)

    @structproperty(int, struct)
    def luck(self):
        return self.field_as_absolute_offset(6)


class StatsEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<HHHHHHHH"

    @property
    def base(self) -> SubStatsEditor:
        return self.field_dispatch(SubStatsEditor, 0)
    @property
    def changes(self) -> SubStatsEditor:
        return self.field_dispatch(SubStatsEditor, 1)
    @property
    def current(self) -> SubStatsEditor:
        return self.field_dispatch(SubStatsEditor, 2)
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


class HealableEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    @structproperty(int, struct)
    def hp(self) -> int:
        return self.field_as_absolute_offset(0)
    @structproperty(int, struct)
    def mp(self) -> int:
        return self.field_as_absolute_offset(1)


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


def affinity_as_map() -> dict[str, Affinity]:
    res = {}
    for i in Affinity:
        res[Affinity(i).name] = Affinity(i)
    return res


AFFINITY_MAP = affinity_as_map()


def affinityprop(fmt):
    return structproperty(
        Affinity, fmt,
        lambda u: Affinity(u),
        lambda t: t.value,
    )    


class AffinityEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    @affinityprop(struct)
    def physical(self) -> int:
        return self.field_as_absolute_offset(0)
    @affinityprop(struct)
    def fire(self) -> int:
        return self.field_as_absolute_offset(1)
    @affinityprop(struct)
    def ice(self) -> int:
        return self.field_as_absolute_offset(2)
    @affinityprop(struct)
    def electric(self) -> int:
        return self.field_as_absolute_offset(3)
    @affinityprop(struct)
    def force(self) -> int:
        return self.field_as_absolute_offset(4)
    @affinityprop(struct)
    def light(self) -> int:
        return self.field_as_absolute_offset(5)
    @affinityprop(struct)
    def dark(self) -> int:
        return self.field_as_absolute_offset(6)
    @affinityprop(struct)
    def poison(self) -> int:
        return self.field_as_absolute_offset(8)
    @affinityprop(struct)
    def confusion(self) -> int:
        return self.field_as_absolute_offset(10)
    @affinityprop(struct)
    def charm(self) -> int:
        return self.field_as_absolute_offset(11)
    @affinityprop(struct)
    def sleep(self) -> int:
        return self.field_as_absolute_offset(12)
    @affinityprop(struct)
    def seal(self) -> int:
        return self.field_as_absolute_offset(13)
    @affinityprop(struct)
    def mirage(self) -> int:
        return self.field_as_absolute_offset(20)


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
    Recovery = auto()
    _UNKNOWN = auto()


def gsproperty(p: PType):
    return property(
        lambda x: x.get(p),
        lambda x, y: x.set(p, y)
    )


class PotentialEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<h"

    def get_absolute_offset(self, t: PType) -> int:
        return self.offset + self.struct_obj.size * t.value

    def get(self, t: PType) -> int:
        return self.struct_obj.unpack_from(
            self.data,
            self.get_absolute_offset(t)
        )[0]

    def set(self, t: PType, potential: int):
        self.struct_obj.pack_into(
            self.data,
            self.get_absolute_offset(t),
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
    recovery = gsproperty(PType.Recovery)
    _unknown = gsproperty(PType._UNKNOWN)


class DemonEditor(BaseDynamicEditor):
    @classmethod
    def id_to_offset(cls, id: int) -> int:
        return DEMON_TABLE_OFFSET + DEMON_ENTRY_SIZE * id

    @property
    def stats(self) -> StatsEditor:
        return self.relative_dispatch(StatsEditor, 0)
    #@property
    #def friendship(self) -> FriendshipEditor:
    #    return self.at_offset(FriendshipEditor, 68)
    @structproperty(int, "<L")
    def friendship(self) -> int:
        return self.relative_as_absolute_offset(68)
    #@structproperty(int, "<H") # , lambda u: bool(u), lambda t: int(t)
    #def is_summoned(self):
    #    return self.relative_offset(72)
    @structproperty(int, "<H")
    def dh_talks(self):
        return self.relative_as_absolute_offset(74)
    @structproperty(int, "<I")
    def is_summoned(self):
        return self.relative_as_absolute_offset(88)
    @property
    def healable(self) -> HealableEditor:
        return self.relative_dispatch(HealableEditor, 100)
    @structproperty(int, "<Q")
    def exp(self) -> int:
        return self.relative_as_absolute_offset(104)
    @structproperty(int, "<B")
    def level(self):
        return self.relative_as_absolute_offset(112)
    #@property
    #def demon_id(self) -> DemonIdEditor:
    #    return self.at_offset(DemonIdEditor, 114)
    @structproperty(int, "<H")
    def demon_id(self):
        return self.relative_as_absolute_offset(114)
    @property
    def skills(self) -> SkillManager:
        return self.relative_dispatch(SkillManager, 120)
    @property
    def affinities(self) -> AffinityEditor:
        return self.relative_dispatch(AffinityEditor, 216)
    @property
    def potentials(self) -> PotentialEditor:
        return self.relative_dispatch(PotentialEditor, 384)
    @property
    def innate_skill(self) -> SkillEditor:
        return self.relative_dispatch(SkillEditor, 408 - calcsize("<I"))

    @property
    def name(self) -> str:
        return DEMON_ID_MAP[self.demon_id]["name"]
