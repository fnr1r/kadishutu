from struct import pack_into, unpack_from
from typing import List, Optional, Tuple

from ..shared.editors import BaseStaticEditor, StructEditor, U8Editor
from .demons import DEMON_TABLE_SIZE


SUMMONED_DEMONS_OFFSET = 0x3d2e


TEAM_TUPLE = Tuple[Optional[int], Optional[int], Optional[int]]


def array_of_fmt(fmt: str, length: int, endianness: str = "<") -> str:
    return endianness + fmt * length


SUMMONED_DEMONS_FMT = array_of_fmt("B", 3)


class DemonOrderEditor(StructEditor):
    fmt = array_of_fmt("B", DEMON_TABLE_SIZE)

    def __get__(self, instance, _) -> List[int]:
        return super().__get__(instance, _)

    def __set__(self, instance, value: List[int]):
        return super().__set__(instance, value)

    def read(self) -> List[int]:
        return list(super().read())
    
    def write(self, v: List[int]):
        super().write(tuple(v))


class TeamEditor(BaseStaticEditor):
    offset = 0
    NO_DEMON = 0xff
    demon_order = DemonOrderEditor(0x3d10)

    @property
    def summoned_demons(self) -> TEAM_TUPLE:
        demons = list(unpack_from(SUMMONED_DEMONS_FMT, self.data, SUMMONED_DEMONS_OFFSET))
        for i in range(len(demons)):
            if demons[i] == self.NO_DEMON:
                demons[i] = None
        return tuple(demons)
    @summoned_demons.setter
    def summoned_demons(self, demons: TEAM_TUPLE):
        from .game import GameSaveEditor
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
