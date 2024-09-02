from enum import Enum, auto
from kadishutu.data.quests import (
    QUEST_ENTRY_SIZE, QUEST_ID_MAP, QUEST_INFO_FIELDS, QUEST_TABLE_OFFSET,
    Quest,
)
from typing import Optional

from ..shared.editors import (
    BaseDynamicEditor, BaseStaticEditor, BaseStructEditor, BoolEditor,
)


# 0x5a760
# 0x5a6c4 - Defeat the Demon King's Armies
# 0x5a628 + 26 * 1 (Quest 88) - The Three Keys
# Entry Size: 26?
# 0x5a65c - NOT USED:mis_info_0089_name
# wa: 0x5a65c - 26 * 89
# 0x59d52 - NOT USED:mis_info_0000_name
# Quest 57: Preta quest


def quest_unused(id: int, attr: str) -> str:
    assert attr in QUEST_INFO_FIELDS
    return f"NOT USED:mis_info_{id:04}_{attr}"


class QuestState(Enum):
    Invalid = 0
    NotStarted = auto()
    InProgress = auto()
    Report = auto()
    Done = auto()


class QuestEditor(BaseDynamicEditor, BaseStructEditor):
    struct = "<?????"
    in_progress = BoolEditor(0)
    done = BoolEditor(1)
    report = BoolEditor(2)
    seen = BoolEditor(3)
    updated = BoolEditor(4)

    @property
    def state(self) -> QuestState:
        in_progress = self.in_progress
        report = self.report
        done = self.done
        if done:
            if report or in_progress:
                return QuestState.Invalid
            return QuestState.Done
        if report:
            if not in_progress:
                return QuestState.Invalid
            return QuestState.Report
        if in_progress:
            return QuestState.InProgress
        return QuestState.NotStarted

    @state.setter
    def state(self, v: QuestState):
        if v == QuestState.Invalid:
            raise ValueError("Invalid is a catch-all and not a valid state")
        if v == QuestState.Done:
            self.in_progress = False
            self.done = True
            self.report = False
            return
        self.done = False
        if v == QuestState.NotStarted:
            self.in_progress = False
            self.report = False
            return
        self.in_progress = True
        self.report = v == QuestState.Report

    def __init__(self, *args, meta: Optional[Quest] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta

    def _offset_to_id(self) -> int:
        (res, chk) = divmod(self.offset - QUEST_TABLE_OFFSET, QUEST_ENTRY_SIZE)
        assert chk == 0
        return res

    @property
    def meta(self) -> Quest:
        if not self._meta:
            self._meta = QUEST_ID_MAP[self._offset_to_id()]
        return self._meta

    @property
    def id(self) -> int:
        return self.meta.id


class QuestManager(BaseStaticEditor):
    offset = QUEST_TABLE_OFFSET

    def at_offset(self, offset: int, *args, **kwargs):
        return self.dispatch(QuestEditor, offset, *args, **kwargs)

    def from_id(self, id: int, *args, **kwargs):
        return self.at_offset(
            self.relative_as_absolute_offset(QUEST_ENTRY_SIZE * id),
            *args,
            **kwargs
        )

    def from_meta(self, meta: Quest):
        return self.at_offset(meta.offset, meta=meta)
