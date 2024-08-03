from datetime import datetime, timedelta
from struct import pack_into, unpack_from
from typing import Optional, Tuple

from .alignment import AlignmentManager
from .dlc import DlcEditor
from .demons import DemonEditor
from .essences import EssenceManager
from .file_handling import BaseEditor, MasterEditor, structproperty
from .items import ItemManager
from .player import PlayerEditor


SUMMONED_DEMONS_FMT = "<BBB"
SUMMONED_DEMONS_OFFSET = 0x3d2e


TEAM_TUPLE = Tuple[Optional[int], Optional[int], Optional[int]]


class TeamEditor(BaseEditor):
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
        save = SaveEditor(self.saveobj)
        # Unset is_summoned flag
        old_demon_list = list(self.summoned_demons)
        print(old_demon_list)
        for i in old_demon_list:
            if i is None:
                continue
            demon = save.demon(i)
            print(demon.name, demon.is_summoned)
            demon.is_summoned = 0
            print(demon.name, demon.is_summoned)
        demon_list = list(demons)
        for i in range(len(demon_list)):
            iv = demon_list[i]
            if iv is None:
                demon_list[i] = self.NO_DEMON
            else:
                save.demon(iv).is_summoned = 1
        pack_into(SUMMONED_DEMONS_FMT, self.data, SUMMONED_DEMONS_OFFSET, *demon_list)
    @structproperty(int, "<B")
    def player_placement(self) -> int:
        return 0x3d45


class SaveEditor(MasterEditor):
    @structproperty(
        datetime, "<Q",
        lambda u: datetime.min + timedelta(microseconds=u/10),
        lambda t: int((t - datetime.min).total_seconds() * (10 ** 7))
    )
    def time_of_saving(self) -> int:
        return 0x4f4
    @property
    def dlc(self) -> DlcEditor:
        return DlcEditor(self.saveobj, 0x529)

    @structproperty(
        timedelta, "<L",
        lambda u: timedelta(seconds=u),
        lambda t: t.seconds
    )
    def play_time(self) -> int:
        return 0x5d0
    @property
    def player(self) -> PlayerEditor:
        return PlayerEditor(self.saveobj, 0)

    def demon(self, id: int) -> DemonEditor:
        if id > 23:
            raise RuntimeWarning(f"Demon {id} data might be invalid")
        return DemonEditor(self.saveobj, id)

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
        return TeamEditor(self.saveobj, 0)

    @structproperty(int, "<H")
    def magatsuhi_gauge(self) -> int:
        return 0x3ece

    @property
    def items(self) -> ItemManager:
        return ItemManager(self.saveobj, 0x4c72)

    @property
    def essences(self) -> EssenceManager:
        return EssenceManager(self.saveobj, 0x4da9)

    @property
    def alignment(self) -> AlignmentManager:
        return AlignmentManager(self.saveobj, 0)
