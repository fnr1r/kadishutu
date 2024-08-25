from struct import unpack_from

from .demons import AffinityEditor, HealableEditor, PotentialEditor, StatsEditor
from .file_handling import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructEditor, U8Editor
)
from .skills import SkillEditor, SkillManager


ENCODING = "UTF-16LE"
NAME_LENGTH = 8


class NameEdit(BaseDynamicEditor, BaseStructEditor):
    length: int
    ikwid: bool

    def __init__(self, master, offset, length: int):
        super().__init__(master, offset)
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


class NameManager(BaseStaticEditor):
    offset = 0
    over_limit = False

    @property
    def save_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 12
        return self.dispatch(NameEdit, 0x4d8, length)

    @property
    def first_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 12
        return self.dispatch(NameEdit, 0x9d0, length)

    @property
    def last_name(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 10
        return self.dispatch(NameEdit, 0x9e8, length)

    @property
    def first_name_again(self) -> NameEdit:
        length = NAME_LENGTH
        if self.over_limit:
            length = 10
        return self.dispatch(NameEdit, 0x9fc, length)

    @property
    def combined_name(self) -> NameEdit:
        length = NAME_LENGTH * 2 + 1
        if self.over_limit:
            length = 20
        return self.dispatch(NameEdit, 0xa10, length)


class PlayerEditor(BaseStaticEditor):
    offset = 0

    names = NameManager.disp()
    stats = StatsEditor.disp(0x988)
    healable = HealableEditor.disp(0x9bc)
    level = U8Editor(0x9c8)
    skills = SkillManager.disp(0xa38)
    affinities = AffinityEditor.disp(0xa98)
    potentials = PotentialEditor.disp(0xb38)
    innate_skill = SkillEditor.disp(0xb4c)
