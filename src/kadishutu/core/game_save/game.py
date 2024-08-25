from dataclasses import dataclass
from enum import Enum, auto
from kadishutu.data.laylines import Layline
from struct import Struct, pack_into, unpack_from
from typing import List, Optional, Tuple

from ..shared.file_handling import (
    BaseMasterEditor, BaseStaticEditor, EnumEditor, TimeDeltaEditor, U16Editor,
    U32Editor, U8Editor, UnrealTimeEditor,
)
from .alignment import AlignmentManager
from .dlc import DlcEditor
from .demons import DemonManager
from .essences import EssenceManager
from .items import ItemManager
from .miracles import MiracleManager
from .miracle_unlocks import MiracleUnlockManager
from .player import PlayerEditor


SUMMONED_DEMONS_FMT = "<BBB"
SUMMONED_DEMONS_OFFSET = 0x3d2e


TEAM_TUPLE = Tuple[Optional[int], Optional[int], Optional[int]]


class TeamEditor(BaseStaticEditor):
    NO_DEMON = 0xff
    @property
    def summoned_demons(self) -> TEAM_TUPLE:
        demons = list(unpack_from(SUMMONED_DEMONS_FMT, self.data, SUMMONED_DEMONS_OFFSET))
        for i in range(len(demons)):
            if demons[i] == self.NO_DEMON:
                demons[i] = None
        return tuple(demons)
    @summoned_demons.setter
    def summoned_demons(self, demons: TEAM_TUPLE):
        assert isinstance(self.master, GameSaveEditor)
        demon_mgr = self.master.demons
        old_demon_list = list(self.summoned_demons)
        for i in old_demon_list:
            if i is None:
                continue
            demon = demon_mgr.in_slot(i)
            demon.is_summoned = 0

        demon_list: List[int] = []
        #demon_icons: List[Tuple[int, int]] = []
        for i in demons:
            if i is None:
                demon_list.append(self.NO_DEMON)
                #demon_icons.append((self.NO_DEMON, 0))
                continue
            demon = demon_mgr.in_slot(i)
            demon.is_summoned = 6
            demon_list.append(demon.slot)
            #demon_icons.append((i.demon_id, i.level))
        pack_into(SUMMONED_DEMONS_FMT, self.data, SUMMONED_DEMONS_OFFSET, *demon_list)
        #demon_icons.insert(self.player_placement, (1, 99))

    player_placement = U8Editor(0x3d45)


@dataclass
class Vector3:
    x: int
    z: int
    y: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.z, self.y)


class PositionEditor(BaseStaticEditor):
    offset = 0
    CORD_OFFSET = 0x568e
    CORD_STRUCT = Struct("<fff")
    ROT_OFFSET = 0x56a6
    ROT_STRUCT = Struct("<ff")

    current_map_upper = U32Editor(0x567e)
    current_map_lower = U32Editor(0x5682)

    @property
    def raw_coordinates(self) -> bytes:
        return bytes(self.data[self.CORD_OFFSET:self.CORD_OFFSET + self.CORD_STRUCT.size])

    @raw_coordinates.setter
    def raw_coordinates(self, value: bytes):
        for i, b in enumerate(value):
            self.data[self.CORD_OFFSET + i] = b

    @property
    def coordinates(self) -> Vector3:
        return Vector3(*self.CORD_STRUCT.unpack(self.raw_coordinates))

    @coordinates.setter
    def coordinates(self, value: Vector3):
        self.raw_coordinates = self.CORD_STRUCT.pack(*value.to_tuple())

    @property
    def raw_rotation(self) -> bytes:
        return bytes(self.data[self.ROT_OFFSET:self.ROT_OFFSET + self.ROT_STRUCT.size])

    @raw_rotation.setter
    def raw_rotation(self, value: bytes):
        for i, b in enumerate(value):
            self.data[self.ROT_OFFSET + i] = b

    @property
    def rotation(self) -> Tuple[int, int]:
        return self.ROT_STRUCT.unpack(self.raw_rotation)

    @rotation.setter
    def rotation(self, pitch: int, yaw: int):
        self.raw_rotation = self.ROT_STRUCT.pack(pitch, yaw)

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


class Difficulty(Enum):
    Safety = 0
    Casual = auto()
    Normal = auto()
    Hard = auto()


class GameSaveEditor(BaseMasterEditor):
    time_of_saving = UnrealTimeEditor(0x4f4)
    difficulty = EnumEditor(0x4fc, Difficulty)
    dlc = DlcEditor.disp()
    play_time = TimeDeltaEditor(0x5d0)
    player = PlayerEditor.disp()
    demons = DemonManager.disp()
    team = TeamEditor.disp()
    macca = U32Editor(0x3d32)
    glory = U32Editor(0x3d4a)
    miracles = MiracleManager.disp()
    magatsuhi_gauge = U16Editor(0x3ece)
    items = ItemManager.disp()
    essences = EssenceManager.disp()
    position = PositionEditor.disp()
    miracle_unlocks = MiracleUnlockManager.disp()
    alignment = AlignmentManager.disp()
