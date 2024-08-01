from struct import calcsize, unpack_from

from .demons import AffinityEditor, HealableEditor, PotentialEditor, StatsEditor
from .file_handling import BaseEditor, BaseStructEditor, structproperty
from .skills import Skill, SkillEditor


ENCODING = "UTF-16LE"
NAME_LENGTH = 8


class NameEdit(BaseStructEditor):
    length: int
    ikwid: bool

    def __init__(self, saveobj, offset, length: int):
        super().__init__(saveobj, offset)
        self.length = length
        self.fmt = f"<{self.blength}s"
        self.ikwid = False

    @property
    def blength(self) -> int:
        return self.length * 2

    def get(self) -> str:
        barray = unpack_from(self.fmt, self.data, self.offset)[0]
        txt = str(barray, encoding=ENCODING)
        return txt

    def raw_set(self, value: bytes):
        for i, byte in enumerate(value):
            self.data[self.offset + i] = byte

    def set(self, value: str):
        assert len(value) <= self.length
        res = value.encode(ENCODING)
        res = res.ljust(self.blength, b"\0")
        # Just to be sure
        assert len(res) <= self.blength
        self.raw_set(res)


class NameManager(BaseEditor):
    over_limit = False

    @property
    def save_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 12
        return NameEdit(self.saveobj, 0x4d8, length)

    @property
    def first_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 12
        return NameEdit(self.saveobj, 0x9d0, length)

    @property
    def last_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 10
        return NameEdit(self.saveobj, 0x9e8, length)

    @property
    def first_name_again(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 10
        return NameEdit(self.saveobj, 0x9fc, length)

    @property
    def combined_name(self) -> NameEdit:
        length = NAME_LENGTH * 2 + 1
        if self.over_limit:
            length = 20
        return NameEdit(self.saveobj, 0xa10, length)


class PlayerEditor(BaseEditor):
    @property
    def names(self) -> NameManager:
        return NameManager(self.saveobj, 0)
    @property
    def stats(self) -> StatsEditor:
        return StatsEditor(self.saveobj, 0x988)
    @property
    def healable(self) -> HealableEditor:
        return HealableEditor(self.saveobj, 0x9bc)
    @structproperty(int, "<B")
    def level(self) -> int:
        return 0x9c8
    @property
    def skills(self) -> SkillEditor:
        return SkillEditor(self.saveobj, 0xa38)
    @property
    def affinities(self) -> AffinityEditor:
        return AffinityEditor(self.saveobj, 0xa98)
    @property
    def potentials(self) -> PotentialEditor:
        return PotentialEditor(self.saveobj, 0xb38)
    @property
    def innate_skill(self) -> Skill:
        return Skill(self.saveobj, 0xb50 - calcsize("<I"))
