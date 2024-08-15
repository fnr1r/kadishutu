from enum import IntFlag, auto
from functools import reduce
from math import log
import operator
from typing import Dict, List
from typing_extensions import Self

from .file_handling import BaseStaticEditor, BaseStructAsSingularValueEditor


DLCS = {
    1: "Safety Difficulty",
    2: "Mitama Dance of Wealth",
    3: "Mitama Dance of EXP",
    4: "Mitama Dance of Glory",
    5: "Holy Will and Profane Dissent",
    6: "Sakura Cinders of the East",
    7: "2 Sacred Treasures Set",
}


DLCS_REV: Dict[str, int] = {}


for k, v in DLCS.items():
    DLCS_REV[v] = k


class DlcBitflags(IntFlag):
    UNUSED = auto()
    DLC_1 = auto()
    DLC_2 = auto()
    DLC_3 = auto()
    DLC_4 = auto()
    DLC_5 = auto()
    DLC_6 = auto()
    DLC_7 = auto()

    @classmethod
    def all(cls) -> Self:
        return cls(0xff) & ~cls.UNUSED

    @classmethod
    def from_str(cls, name: str) -> Self:
        return cls(1 << DLCS_REV[name])

    def get_flags(self) -> List[str]:
        return [DLCS[int(log(i.value, 2))] for i in self]

    @classmethod
    def from_flags(cls, flags: List[str]) -> Self:
        return reduce(operator.or_, [
            cls.from_str(flag)
            for flag in flags
        ], cls(0))


class DlcEditor(BaseStaticEditor, BaseStructAsSingularValueEditor):
    offset = 0x529
    struct = "<B"

    def get(self) -> DlcBitflags:
        return DlcBitflags(self.value)

    def set(self, value: DlcBitflags):
        self.value = value.value

    flags = property(lambda x: x.get(), lambda x, y: x.set(y))

    def clear(self):
        self.flags = DlcBitflags(0)

    @staticmethod
    def flags_from_name(name: str) -> DlcBitflags:
        return DlcBitflags.from_str(name)
