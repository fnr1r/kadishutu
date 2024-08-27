from enum import Enum, auto
from kadishutu.data.affinity import Affinity
from kadishutu.data.demons import DEMON_ID_MAP, Demon

from ..shared.file_handling import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructAsFieldEditor, U16Editor,
    U32Editor, U64Editor, U8Editor, structproperty,
)
from .skills import SkillEditor, SkillManager


DEMON_TABLE_OFFSET = 0xb60
DEMON_ENTRY_SIZE = 424
DEMON_TABLE_SIZE = 30
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
        assert not self.struct_obj.unpack_from(self.data, self.field_as_absolute_offset(7))[0], \
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

    def recalculate(self):
        # TODO: Take skills into account
        for stat in STATS_NAMES:
            stat = stat.lower()
            base = self.base.__getattribute__(stat)
            changes = self.changes.__getattribute__(stat)
            self.current.__setattr__(stat, base + changes)


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


def affinityprop(fmt):
    return structproperty(
        Affinity, fmt,
        lambda u: Affinity(u),
        lambda t: t.value,
    ) 


class AffinityEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    @affinityprop(struct)
    def physical_copy(self) -> int:
        return self.field_as_absolute_offset(0)
    @affinityprop(struct)
    def fire_copy(self) -> int:
        return self.field_as_absolute_offset(1)
    @affinityprop(struct)
    def ice_copy(self) -> int:
        return self.field_as_absolute_offset(2)
    @affinityprop(struct)
    def electric_copy(self) -> int:
        return self.field_as_absolute_offset(3)
    @affinityprop(struct)
    def force_copy(self) -> int:
        return self.field_as_absolute_offset(4)
    @affinityprop(struct)
    def light_copy(self) -> int:
        return self.field_as_absolute_offset(5)
    @affinityprop(struct)
    def dark_copy(self) -> int:
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
    @affinityprop(struct)
    def physical(self) -> int:
        return self.field_as_absolute_offset(28)
    @affinityprop(struct)
    def fire(self) -> int:
        return self.field_as_absolute_offset(29)
    @affinityprop(struct)
    def ice(self) -> int:
        return self.field_as_absolute_offset(30)
    @affinityprop(struct)
    def electric(self) -> int:
        return self.field_as_absolute_offset(31)
    @affinityprop(struct)
    def force(self) -> int:
        return self.field_as_absolute_offset(32)
    @affinityprop(struct)
    def light(self) -> int:
        return self.field_as_absolute_offset(33)
    @affinityprop(struct)
    def dark(self) -> int:
        return self.field_as_absolute_offset(34)


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
    #_UNKNOWN = auto()


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
    #_unknown = gsproperty(PType._UNKNOWN)


class DemonEditor(BaseDynamicEditor):
    @property
    def meta(self) -> Demon:
        return DEMON_ID_MAP[self.demon_id]

    stats = StatsEditor.disp(0)
    friendship = U32Editor(0x44)
    @structproperty(int, "<H")
    def dh_talks(self):
        return self.relative_as_absolute_offset(74)
    is_summoned = U32Editor(0x60)
    healable = HealableEditor.disp(0x64)
    exp = U64Editor(0x68)
    level = U8Editor(0x70)
    demon_id = U16Editor(0x72)
    skills = SkillManager.disp(0x78)
    affinities = AffinityEditor.disp(0xd8)
    potentials = PotentialEditor.disp(0x180)
    innate_skill = SkillEditor.disp(0x194)

    @property
    def name(self) -> str:
        return self.meta.name

    @property
    def is_free(self) -> bool:
        return self.demon_id == 0xffff

    @property
    def slot(self) -> int:
        dtoff = self.offset - DEMON_TABLE_OFFSET
        assert not dtoff % DEMON_ENTRY_SIZE, "Misaligned demon entry"
        return dtoff // DEMON_ENTRY_SIZE

    @property
    def raw(self) -> bytearray:
        end = self.offset + DEMON_ENTRY_SIZE
        return self.data[self.offset:end]


class DemonManager(BaseStaticEditor):
    offset = DEMON_TABLE_OFFSET
    DEMON_STORAGE = 24

    def at_offset(self, offset: int, *args, **kwargs) -> DemonEditor:
        return self.dispatch(DemonEditor, offset, *args, **kwargs)

    def in_slot(self, id: int, *args, **kwargs) -> DemonEditor:
        return self.at_offset(
            self.relative_as_absolute_offset(DEMON_ENTRY_SIZE * id),
            *args,
            **kwargs
        )

    def __iter__(self):
        for i in range(self.DEMON_STORAGE):
            yield self.in_slot(i)

    def enumerate(self):
        for i in range(self.DEMON_STORAGE):
            yield (i, self.in_slot(i))

    def real(self):
        for demon in self:
            if not demon.is_free:
                yield demon

    def _find_free_slot(self) -> DemonEditor:
        for demon in self:
            if demon.is_free:
                return demon
        raise RuntimeError

    def new_from_initial(self, meta: Demon) -> DemonEditor:
        print("USING EXPERIMENTAL METHOD new_from_initial")
        demon = self._find_free_slot()
        demon.demon_id = meta.id
        demon.level = meta.level
        stats = demon.stats
        for stat in STATS_NAMES:
            stat = stat.lower()
            stats.base.__setattr__(stat, meta.stats.__getattribute__(stat))
        stats.recalculate()
        for i, skill in enumerate(meta.skills):
            demon.skills.slot(i).id = skill.id
        demon.innate_skill.id = meta.innate_skill.id
        affinities = demon.affinities
        for i in AFFINITY_NAMES:
            i = i.lower()
            affinities.__setattr__(i, meta.affinities.__getattribute__(i))
        potentials = demon.potentials
        for i in PType:
            potentials.set(i, meta.potentials.__getattribute__(i.name.lower()))
        return demon

    #def new_from_compendium(self, meta) -> DemonEditor:
    #    raise NotImplementedError
