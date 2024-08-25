from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from struct import Struct, pack_into, unpack_from
from typing import List, Optional, Tuple

from .alignment import AlignmentManager
from .data.laylines import Layline
from .dlc import DlcEditor
from .demons import DemonManager
from .essences import EssenceManager
from .file_handling import BaseMasterEditor, BaseStaticEditor, EditorGetter, structproperty
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
        assert isinstance(self.master, SaveEditor)
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

    @structproperty(int, "<B")
    def player_placement(self) -> int:
        return 0x3d45


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

    @structproperty(int, "<I")
    def current_map_upper(self) -> int:
        return 0x567e

    @structproperty(int, "<I")
    def current_map_lower(self) -> int:
        return 0x5682

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

    @structproperty(int, "<B")
    def last_layline_fount(self) -> int:
        return 0x68c5

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


def unreal_to_python_datetime(ticks: int) -> datetime:
    return datetime.min + timedelta(microseconds=ticks/10)


def python_to_unreal_datetime(time: datetime) -> int:
    return int((time - datetime.min).total_seconds() * (10 ** 7))


class SaveEditor(BaseMasterEditor):
    @structproperty(
        datetime, "<Q", unreal_to_python_datetime, python_to_unreal_datetime,
    )
    def time_of_saving(self) -> int:
        return 0x4f4

    @structproperty(
        Difficulty, "<B",
        lambda u: Difficulty(u),
        lambda t: t.value
    )
    def difficulty(self) -> int:
        return 0x4fc

    @property
    def dlc(self) -> DlcEditor:
        return self.dispatch(DlcEditor)

    @structproperty(
        timedelta, "<L",
        lambda u: timedelta(seconds=u),
        lambda t: t.seconds
    )
    def play_time(self) -> int:
        return 0x5d0
    @property
    def player(self) -> PlayerEditor:
        return self.dispatch(PlayerEditor)

    @property
    def demons(self) -> DemonManager:
        return self.dispatch(DemonManager)

    #MACCA = Struct("<I")
    #@property
    #def macca(self) -> int:
    #    return self.MACCA.unpack_from(self.savefile.data, 0x3d32)[0]
    #@macca.setter
    #def macca(self, value: int):
    #    self.MACCA.pack_into(self.savefile.data, 0x3d32, value)
    #maccaf = structproperty(int, "<I", 0x3d32)
    @structproperty(int, "<I")
    def macca(self) -> int:
        return 0x3d32
    @structproperty(int, "<I")
    def glory(self) -> int:
        return 0x3d4a

    @property
    def team(self) -> TeamEditor:
        return self.dispatch(TeamEditor)

    @property
    def miracles(self) -> MiracleManager:
        return self.dispatch(MiracleManager)

    @structproperty(int, "<H")
    def magatsuhi_gauge(self) -> int:
        return 0x3ece

    @property
    def items(self) -> ItemManager:
        return self.dispatch(ItemManager)

    @property
    def essences(self) -> EssenceManager:
        return self.dispatch(EssenceManager)

    @property
    def position(self) -> PositionEditor:
        return self.dispatch(PositionEditor)
    
    @property
    def miracle_unlocks(self) -> MiracleUnlockManager:
        return self.dispatch(MiracleUnlockManager)

    @property
    def alignment(self) -> AlignmentManager:
        return self.dispatch(AlignmentManager)
