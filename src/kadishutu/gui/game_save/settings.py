from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from kadishutu.core.game_save.game import Difficulty

from ..shared import AppliableWidget, MComboBox, hboxed
from .shared import GameScreenMixin


class SettingsEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout(self)
        self.difficulty = MComboBox()
        self.difficulty.addItems([
            difficulty.name
            for difficulty in Difficulty
        ])
        self.l.addLayout(hboxed(
            QLabel("Difficulty"), self.difficulty
        ))
        self.l.addStretch()

    def stack_refresh(self):
        self.difficulty.setCurrentText(self.save.difficulty.name)

    def _apply_difficulty(self, value: str):
        self.save.difficulty = Difficulty[value]

    def on_apply_changes(self):
        self.difficulty.update_if_modified(self._apply_difficulty)
