from dataclasses import dataclass, field
from kadishutu.tools.groupobj import group_objects
from kadishutu.tools.eprint import printexcept
from kadishutu.tools.tbbreader import Tbcr
from kadishutu.tools.uexp_extract import UExpTranslationFile
from struct import calcsize
from typing import List, Union
from typing_extensions import Self

from .miracles import UMODEL_SAVED_PATH, Destructable
from .tools.mapping import make_maps


QUEST_TABLE_OFFSET = 0x59d52
QUEST_ENTRY_SIZE = 26
QUEST_INFO_FIELDS = [
    "name", "client", "reward", "explain", "help", "report", "completed",
]


@dataclass
class QuestStrings:
    name: str
    client: str
    reward: str
    explain: str
    helpstr: str
    report: str
    completed: str

    PATH = "Game/L10N/en/Blueprints/Gamedata/BinTable/Mission/MissionInfo.uexp"

    @classmethod
    def _data_fixup(cls, uexp: UExpTranslationFile) -> List[str]:
        lcopy = uexp.textl[3:]

        def insert_at(i: int, j: str, txt: str = ""):
            lcopy.insert(7 * i + QUEST_INFO_FIELDS.index(j), txt)

        insert_at(147, "reward", "None")
        insert_at(148, "reward", "None")

        return lcopy

    @classmethod
    def from_uexp(cls, uexp: UExpTranslationFile) -> List[Self]:
        strlist = cls._data_fixup(uexp)
        return [
            cls(*i)
            for i in group_objects(strlist, len(QUEST_INFO_FIELDS))
        ]

    @classmethod
    def from_path(cls) -> List[Self]:
        path = UMODEL_SAVED_PATH / cls.PATH
        try:
            uexp = UExpTranslationFile.from_path(path)
        except FileNotFoundError:
            return []
        return cls.from_uexp(uexp)


QUEST_STRINGS = QuestStrings.from_path()


TABLE_SIZE = 0x14580
TABLE_ROW_SIZE = 0x174


def struct_padded(txt: str, size: int) -> str:
    r = size - calcsize(txt)
    assert r > 0
    return txt + f"{r}s"


@dataclass
class QuestData(Destructable):
    id: int
    unknown_data: bytes = field(repr=False)

    def get_format(*args, **kwargs) -> Union[str, bytes]:
        return struct_padded("<H", TABLE_ROW_SIZE)


try:
    tcx = Tbcr.from_path(UMODEL_SAVED_PATH / "Game/Blueprints/Gamedata/BinTable/Mission/MissionTable.uexp")
    QUEST_DATA = QuestData.from_array_of_bytes(tcx.tables[0].rows)
except Exception as e:
    printexcept("Failed to load quest data", e)
    QUEST_DATA = []


@dataclass
class Quest:
    data: QuestData
    strings: QuestStrings

    @classmethod
    def load_quests(cls) -> List[Self]:
        if not QUEST_STRINGS or not QUEST_DATA:
            return []
        return [
            cls(*i)
            for i in list(zip(QUEST_DATA, QUEST_STRINGS))
        ]

    @property
    def id(self) -> int:
        return self.data.id

    @property
    def name(self) -> str:
        # TODO: Format the name
        return self.strings.name

    @name.setter
    def name(self, v: str):
        self.strings.name = v

    @property
    def offset(self) -> int:
        return QUEST_TABLE_OFFSET + QUEST_ENTRY_SIZE * self.id


QUESTS = Quest.load_quests()


(QUEST_ID_MAP, QUEST_NAME_MAP) = make_maps(QUESTS)
