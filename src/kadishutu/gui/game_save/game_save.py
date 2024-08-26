from kadishutu.core.game_save import GameSaveEditor
from kadishutu.core.shared.file_handling import DecryptedSave
from pathlib import Path
from PySide6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QWidget,
)

from ..shared import (
    QU32, AppliableWidget, SaveScreenMixin, hboxed,
)
from .alignment import AlignmentEditorScreen
from .demons import DemonSelectorScreen
from .dlc import DlcEditorScreen
from .essences import EssenceEditorScreen
from .items import ItemEditorScreen
from .miracles import MiracleEditorScreen
from .player import PlayerEditorScreen
from .settings import SettingsEditorScreen
from .teleport import TeleporterScreen


class GameSaveEditorScreen(SaveScreenMixin, QWidget, AppliableWidget):
    path: Path
    raw_save: DecryptedSave
    save: GameSaveEditor
    modified: bool

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.save = GameSaveEditor(self.raw_save)

        self.l = QVBoxLayout(self)
        self.macca = QU32()
        self.l.addLayout(hboxed(QLabel("Macca"), self.macca))
        self.glory = QU32()
        self.l.addLayout(hboxed(QLabel("Glory"), self.glory))

        for name, cls in [
            ("DLC", DlcEditorScreen),
            ("Player", PlayerEditorScreen),
            ("Demons", DemonSelectorScreen),
            ("Miracles", MiracleEditorScreen),
            ("Items", ItemEditorScreen),
            ("Essences", EssenceEditorScreen),
            ("Layline Crossing", TeleporterScreen),
            ("Alignment", AlignmentEditorScreen),
            ("Settings", SettingsEditorScreen),
        ]:
            widget = QPushButton(name)
            widget.clicked.connect(self.spawner(cls))
            self.l.addWidget(widget)

        self.l.addStretch()

    def stack_refresh(self):
        self.macca.setValue(self.save.macca)
        self.glory.setValue(self.save.glory)

    def on_apply_changes(self):
        self.macca.setattr_if_modified(self.save, "macca")
        self.glory.setattr_if_modified(self.save, "glory")
