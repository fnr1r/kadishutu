from enum import Enum, auto
from kadishutu.data.demons import DEMON_ID_MAP, Demon

from ..shared.file_handling import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructAsFieldEditor, U16Editor,
    U32Editor, U64Editor, U8Editor, structproperty,
)
from .affinities import (
    AILMENT_AFFINITY_NAMES, ELEMENTAL_AFFINITY_NAMES, AffinityManager,
)
from .skills import SkillEditor, SkillManager
from .stats import STATS_NAMES, HealableEditor, StatBlockEditor


DEMON_TABLE_OFFSET = 0xb60
DEMON_ENTRY_SIZE = 424
DEMON_TABLE_SIZE = 30
STAT_TABLE_SIZE = 16


META_POTENTIALS = ("<hhhhhhhhhhhh", "PHYSICAL FIRE ICE ELECTRIC FORCE LIGHT DARK ALMIGHTY AILMENT SUPPORT HEALING _unknown")


#class FriendshipEditor(BaseStructEditor):
#    fmt = "<L"
#
#    def get(self) -> int:
#        return self.unpack()[0]
#
#    def set(self, id: int):
#        self.pack(id)


#class DemonIdEditor(SingularIntEditor):
#    fmt = "<H"
#
#    @property
#    def name_table(self) -> Dict[int, str]:
#        return DEMONS


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

    stats = StatBlockEditor.rdisp(0)
    friendship = U32Editor(0x44)
    @structproperty(int, "<H")
    def dh_talks(self):
        return self.relative_as_absolute_offset(74)
    is_summoned = U32Editor(0x60)
    healable = HealableEditor.rdisp(0x64)
    exp = U64Editor(0x68)
    level = U8Editor(0x70)
    demon_id = U16Editor(0x72)
    skills = SkillManager.rdisp(0x78)
    affinities = AffinityManager.rdisp(0xd8)
    potentials = PotentialEditor.rdisp(0x180)
    innate_skill = SkillEditor.rdisp(0x194)

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
        orig_elem = affinities.original_elemental
        cur_elem = affinities.current_elemental
        for i in ELEMENTAL_AFFINITY_NAMES:
            i = i.lower()
            aff = meta.affinities.__getattribute__(i)
            orig_elem.__setattr__(i, aff)
            cur_elem.__setattr__(i, aff)
        cur_ailm = affinities.ailment
        for i in AILMENT_AFFINITY_NAMES:
            i = i.lower()
            aff = meta.affinities.__getattribute__(i)
            cur_ailm.__setattr__(i, aff)
        potentials = demon.potentials
        for i in PType:
            potentials.set(i, meta.potentials.__getattribute__(i.name.lower()))
        return demon

    #def new_from_compendium(self, meta) -> DemonEditor:
    #    raise NotImplementedError
