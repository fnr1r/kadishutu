from enum import Enum, auto

from ..shared.file_handling import (
    BaseMasterEditor, EnumEditor, TimeDeltaEditor, U16Editor, U32Editor,
    UnrealTimeEditor,
)
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
    compendium = CompendiumManager.disp()
    quests = QuestManager.disp()
    alignment = AlignmentManager.disp()
