from enum import Enum, auto

from ..shared.editors import (
    BaseDynamicEditor, BaseStructAsFieldEditor, I16Editor,
)


class PotentialType(Enum):
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


class PotentialEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<h"

    def get_absolute_offset(self, t: PotentialType) -> int:
        return self.field_as_absolute_offset(t.value)

    def read(self, t: PotentialType) -> int:
        return self.struct_obj.unpack_from(
            self.data,
            self.get_absolute_offset(t)
        )[0]

    def write(self, t: PotentialType, potential: int):
        self.struct_obj.pack_into(
            self.data,
            self.get_absolute_offset(t),
            potential
        )

    physical = I16Editor(0)
    fire = I16Editor(0x2)
    ice = I16Editor(0x4)
    electric = I16Editor(0x6)
    force = I16Editor(0x8)
    light = I16Editor(0xa)
    dark = I16Editor(0xc)
    almighty = I16Editor(0xe)
    ailment = I16Editor(0x10)
    support = I16Editor(0x12)
    recovery = I16Editor(0x14)
    #_unknown = gsproperty(PType._UNKNOWN)
