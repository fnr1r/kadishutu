from dataclasses import dataclass
from struct import calcsize
from typing import Tuple

from typing_extensions import Self

from kadishutu.data.laylines import Layline

from ..shared.editors import (
    BaseStaticEditor, BytesEditor, StructEditor, U32Editor, U8Editor,
)


FLOAT_SET = Tuple[float, float, float]


@dataclass
class Vector3:
    """
    More info on the coordinate system of Unreal Engine:
    
    https://dev.epicgames.com/documentation/en-us/unreal-engine/coordinate-system-and-spaces-in-unreal-engine
    """
    x: float
    y: float
    z: float

    @classmethod
    def from_tuple(cls, x: float, y: float, z: float) -> Self:
        return cls(x, y, z)

    def to_tuple(self) -> FLOAT_SET:
        return (self.x, self.y, self.z)


class FloatSetEditor(StructEditor):
    fmt = "<fff"

    def read(self) -> FLOAT_SET:
        return super().read()
    
    def write(self, v: FLOAT_SET):
        super().write(v)


class Vector3Editor(FloatSetEditor):
    def read(self) -> Vector3:
        return Vector3.from_tuple(*super().read())
    
    def write(self, v: Vector3):
        super().write(v.to_tuple())


class RotationEditor(StructEditor):
    fmt = "<ff"

    def read(self) -> Tuple[float, float]:
        return super().read()
    
    def write(self, v: Tuple[float, float]):
        super().write(v)


CORD_OFFSET = 0x568e
ROT_OFFSET = 0x56a6


class PositionEditor(BaseStaticEditor):
    offset = 0

    title_save_location = U32Editor(0x524)
    current_map_upper = U32Editor(0x567e)
    current_map_lower = U32Editor(0x5682)
    raw_coordinates = BytesEditor(CORD_OFFSET, calcsize(FloatSetEditor.fmt))
    coordinates = Vector3Editor(CORD_OFFSET)
    raw_rotation = BytesEditor(ROT_OFFSET, calcsize(RotationEditor.fmt))
    rotation = RotationEditor(ROT_OFFSET)
    last_layline_fount = U8Editor(0x68c5)

    def layline_unlock(self, layline: Layline):
        (offset, bit) = layline.unlock_data
        self.data[offset] |= 1 << bit

    def layline_teleport(self, layline: Layline, unlock: bool = True):
        self.raw_coordinates = layline.coordinates
        self.raw_rotation = layline.rotation
        self.current_map_upper = layline.map_upper
        self.current_map_lower = layline.map_lower
        self.last_layline_fount = layline.id
        if unlock:
            self.layline_unlock(layline)
