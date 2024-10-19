from kadishutu.core.game_save.game import Endings
from typing import Callable, Dict
from PySide6.QtWidgets import QLabel, QGridLayout, QWidget

from ..shared import QU8, AppliableWidget, MCheckBox
from .shared import GameScreenMixin



class CrossCycleEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ending_map: Dict[Endings, MCheckBox] = {}

        self.l = QGridLayout(self)
        i = 0

        label = QLabel("Clear")
        self.l.addWidget(label, i, 0)
        self.clear_box = MCheckBox()
        self.l.addWidget(self.clear_box, i, 1)
        i += 1

        label = QLabel("Cycles")
        self.l.addWidget(label, i, 0)
        self.cycles_box = QU8()
        self.l.addWidget(self.cycles_box, i, 1)
        i += 1

        label = QLabel("Endings")
        self.l.addWidget(label, i, 0, 2, 1)
        i += 1
        endingsl = QGridLayout()
        self.l.addLayout(endingsl, i, 0, 2, 1)
        for j, end in enumerate(Endings):
            assert end.name
            name = end.name
            endingsl.addWidget(QLabel(name), j, 0)
            end_box = MCheckBox()
            endingsl.addWidget(end_box, j, 1)
            self.ending_map[end] = end_box

    def stack_refresh(self):
        self.clear_box.setChecked(self.save.clear_flag)
        self.clear_box.set_modified(False)
        self.cycles_box.setValue(self.save.cycles)
        for k, v in self.ending_map.items():
            v.setChecked(self.save.endings & k)

    def on_apply_changes(self):
        self.clear_box.setattr_if_modified(self.save, "clear_flag")
        self.cycles_box.setattr_if_modified(self.save, "cycles", "cycles_copy")
        def update_cb(v: Endings) -> Callable[[bool], None]:
            def wrapped(box: bool):
                if box:
                    self.save.endings |= v
                else:
                    self.save.endings &= ~v
                self.save.endings_copy = self.save.endings
            return wrapped
        for k, v in self.ending_map.items():
            v.update_if_modified(update_cb(k))
