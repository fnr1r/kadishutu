from typing import Optional, Tuple, Union

from kadishutu.core.game_save.affinities import AffinityManager
from kadishutu.core.game_save.potentials import PotentialEditor
from kadishutu.data.demons import DEMON_ID_MAP, DEMON_NAME_MAP, Demon
from kadishutu.data.skills import SKILL_ID_MAP, Skill

from ..shared.editors import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructAsFieldEditor, BoolEditor,
    U16Editor, U8Editor,
)
from .stats import StatsEditor


COMPENDIUM_OFFSET = 0x18272
COMPENDIUM_ENTRY_SIZE = 0xe0


def demon_id_to_compendium_offset(demon_id: int) -> int:
    return COMPENDIUM_OFFSET + demon_id * COMPENDIUM_ENTRY_SIZE


def comp_to_demon_id(offset: int) -> int:
    (res, remainder) = divmod(
        offset - COMPENDIUM_OFFSET,
        COMPENDIUM_ENTRY_SIZE
    )
    assert remainder == 0
    return res


class CompSkillEditor(BaseDynamicEditor):
    id = U16Editor(0)

    @property
    def meta(self) -> Skill:
        return SKILL_ID_MAP[self.id]


class CompSkillManager(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    def slot(self, no: int) -> CompSkillEditor:
        return self.field_dispatch(CompSkillEditor, no)

    def __getitem__(self, indices: Union[int, Tuple[int, ...]]):
        if isinstance(indices, tuple):
            raise NotImplementedError
        return self.slot(indices)


class RegisteredDemonEditor(BaseDynamicEditor):
    def __init__(self, *args, meta: Optional[Demon] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta

    @property
    def meta(self) -> Demon:
        if not self._meta:
            self._meta = DEMON_ID_MAP[comp_to_demon_id(self.offset)]
        return self._meta

    stat_original = StatsEditor.rdisp(0)
    stat_changes = StatsEditor.rdisp(0x10)
    skills = CompSkillManager.rdisp(0x40)
    level = U8Editor(0x54)
    registered = BoolEditor(0x56)
    affinities = AffinityManager.rdisp(0x58)
    potentials = PotentialEditor.rdisp(0x90)
    innate_skill = CompSkillEditor.rdisp(0xc2)


class CompendiumManager(BaseStaticEditor):
    offset = COMPENDIUM_OFFSET

    def at_offset(self, offset: int, *args, **kwargs) -> RegisteredDemonEditor:
        return self.dispatch(RegisteredDemonEditor, offset, *args, **kwargs)

    def from_id(self, id: int, *args, **kwargs) -> RegisteredDemonEditor:
        return self.at_offset(
            demon_id_to_compendium_offset(id),
            *args, **kwargs,
        )

    def from_meta(self, demon: Demon) -> RegisteredDemonEditor:
        return self.from_id(
            demon.id,
            meta=demon
        )

    def from_name(self, name: str) -> RegisteredDemonEditor:
        return self.from_meta(DEMON_NAME_MAP[name])
