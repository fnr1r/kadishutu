from enum import Enum, IntFlag, auto

from ..shared.editors import (
    BaseMasterEditor, BoolEditor, EnumEditor, TimeDeltaEditor, U16Editor, U32Editor,
    U8Editor, UnrealTimeEditor,
)
from ..shared.unreal_editors import UnrealInternalEditor
from .alignment import AlignmentManager
from .compendium import CompendiumManager
from .dlc import DlcEditor
from .demons import DemonManager
from .essences import EssenceManager
from .items import ItemManager
from .miracles import MiracleManager
from .miracle_unlocks import MiracleUnlockManager
from .player import PlayerEditor
from .position import PositionEditor
from .quests import QuestManager
from .team import TeamEditor


class Difficulty(Enum):
    Safety = 0
    Casual = auto()
    Normal = auto()
    Hard = auto()


class Endings(IntFlag):
    CreationNeutral = auto()
    CreationLaw = auto()
    CreationChaos = auto()
    CreationSecret = auto()
    VengeanceLaw = auto()
    VengeanceChaos = auto()


class GameSaveEditor(BaseMasterEditor):
    unreal_engine_internals = UnrealInternalEditor.disp()
    # Pre-loaded section
    time_of_saving = UnrealTimeEditor(0x4f4)
    difficulty = EnumEditor(0x4fc, Difficulty)
    cycles_copy = U8Editor(0x502)
    endings_copy = EnumEditor(0x503, Endings)
    clear_flag = BoolEditor(0x528)
    dlc = DlcEditor.disp()
    play_time = TimeDeltaEditor(0x5d0)
    # End of pre-loaded section
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
    compendium = CompendiumManager.disp()
    quests = QuestManager.disp()
    alignment = AlignmentManager.disp()
    cycles = U8Editor(0x6a08a)
    endings = EnumEditor(0x6a08b, Endings)

    def erase_demon(self, slot: int, skip_if_free: bool = True):
        from .demons import DEMON_ENTRY_SIZE

        demon = self.demons.in_slot(slot)
        if skip_if_free and demon.is_free:
            return

        team = self.team

        # Desummon
        summoned = list(team.summoned_demons)
        for i in range(3):
            if summoned[i] != slot:
                continue
            summoned[i] = None
        self.team.summoned_demons = tuple(summoned) # type: ignore

        # Remove from demon list
        order = team.demon_order
        for i in range(30):
            if order[i] != slot:
                continue
            order[i] = 0xff
        self.team.demon_order = order

        # Erase data
        demon.erase()
