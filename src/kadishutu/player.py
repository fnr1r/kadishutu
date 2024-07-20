from struct import pack_into, unpack_from

from .demons import AffinityEditor, HealableEditor, PotentialEditor, StatsEditor
from .file_handling import BaseEditor, structproperty
from .skills import SkillEditor


ENCODING = "UTF-16"
# 8 chars
NAME_LENGTH = 8
NAME_LENGTH_BYTES = NAME_LENGTH * 2
COMBINED_NAMES_LENGTH_BYTES = NAME_LENGTH_BYTES + 4
NAME_FMT = f"<{NAME_LENGTH_BYTES}s"
FIRST_NAME_OFFSETS = [0x4d8, 0x9d0, 0x9fc]
LAST_NAME_OFFSET = 0x9e8
NAMES_COMBINED_FMT = f"<{COMBINED_NAMES_LENGTH_BYTES}s"
NAMES_COMBINED_OFFSET = 0xa10


class PlayerEditor(BaseEditor):
    @property
    def first_name(self) -> str:
        copies = [
            unpack_from(NAME_FMT, self.data, i)[0]
            for i in FIRST_NAME_OFFSETS
        ]
        assert copies[0] == copies[1] and copies[1] == copies[2]
        return str(copies[0], encoding=ENCODING)
    @first_name.setter
    def first_name(self, value: str):
        assert len(value) <= NAME_LENGTH
        res = value.encode(ENCODING).zfill(NAME_LENGTH_BYTES)
        for i in FIRST_NAME_OFFSETS:
            pack_into(NAME_FMT, self.data, i, res)
        self.combined_names_update()
    @property
    def last_name(self) -> str:
        return str(unpack_from(NAME_FMT, self.data, LAST_NAME_OFFSET)[0], encoding=ENCODING)
    @last_name.setter
    def last_name(self, value: str):
        assert len(value) <= NAME_LENGTH
        res = value.encode(ENCODING).zfill(NAME_LENGTH_BYTES)
        pack_into(NAME_FMT, self.data, LAST_NAME_OFFSET, res)
        self.combined_names_update()
    def combined_names_update(self):
        # TODO: Fix this
        # This should work fine, but it doesn't.
        res = "{} {}".format(self.first_name, self.last_name)
        res = res.encode(ENCODING).zfill(COMBINED_NAMES_LENGTH_BYTES)
        pack_into(NAMES_COMBINED_FMT, self.data, NAMES_COMBINED_OFFSET, res)
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
