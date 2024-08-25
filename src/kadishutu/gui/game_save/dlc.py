from kadishutu.core.game_save.dlc import DLCS, DlcBitflags
from typing import Dict
from PySide6.QtWidgets import QCheckBox, QGridLayout, QLabel, QWidget

from ..shared import AppliableWidget
from .shared import GameScreenMixin


class DlcEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets: Dict[str, QCheckBox] = {}

        self.l = QGridLayout(self)

        for i, dlc in enumerate(DLCS.values()):
            label = QLabel(dlc)
            self.l.addWidget(label, i, 0)
            dlc_box = QCheckBox()
            self.l.addWidget(dlc_box, i, 1)
            self.widgets[dlc] = dlc_box

    def stack_refresh(self):
        dlcs = self.save.dlc.flags.get_flags()
        for name, dlc_box in self.widgets.items():
            dlc_box.setChecked(name in dlcs)

    def on_apply_changes(self):
        dlcs = [
            name
            for name, dlc_box in self.widgets.items()
            if dlc_box.isChecked()
        ]
        self.save.dlc.flags = DlcBitflags.from_flags(dlcs)
