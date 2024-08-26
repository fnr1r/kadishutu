from kadishutu.data.laylines import LAYLINE_DATA, LAYLINE_NAME_MAP
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget
)

from ..shared import AppliableWidget
from .shared import GameScreenMixin


NOTE_MSG = "NOTE: The save location is not changed."


class TeleporterScreen(QWidget, GameScreenMixin, AppliableWidget):
    NO_VALUE = "NONE"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout(self)

        self.l.addWidget(QLabel(NOTE_MSG))

        self.location_box = QComboBox()
        self.location_box.addItem(self.NO_VALUE)
        self.location_box.addItems([
            i.name
            for i in LAYLINE_DATA
        ])
        self.location_box.currentTextChanged.connect(self.on_place_changed)
        self.l.addWidget(self.location_box)

        self.unlock_layline = QCheckBox("Unlock layline")
        self.unlock_layline.setChecked(True)
        self.l.addWidget(self.unlock_layline)

        self.button = QPushButton("Teleport")
        self.button.setEnabled(False)
        self.button.clicked.connect(self.main_window.on_apply)
        self.l.addWidget(self.button)

    def on_place_changed(self, name: str):
        if name == self.NO_VALUE:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def stack_refresh(self):
        self.location_box.setCurrentText(self.NO_VALUE)

    def on_apply_changes(self):
        location_name = self.location_box.currentText()
        if location_name == self.NO_VALUE:
            return
        try:
            layline = LAYLINE_NAME_MAP[location_name]
        except KeyError:
            return
        position = self.save.position
        position.layline_teleport(layline, self.unlock_layline.isChecked())
        self.stack_remove()
