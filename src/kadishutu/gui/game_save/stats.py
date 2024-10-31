from typing import Dict

from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget

from kadishutu.core.game_save.stats import (
    STATS_NAMES, HealableEditor, StatBlockEditor,
)

from ..shared import QU16, AppliableWidget
from .shared import GameScreenMixin


class StatEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    STAT_TYPES = ["Base", "Changes", "Current", "Healable"]

    def __init__(
        self,
        stats: StatBlockEditor,
        healable: HealableEditor,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.stats = stats
        self.healable = healable
        self.labels = []
        self.widgets: Dict[str, Dict[str, QU16]] = {}

        self.l = QGridLayout(self)

        for i in range(0, 4):
            text = self.STAT_TYPES[i]
            l = QLabel(text)
            self.l.addWidget(l, 0, i + 1)
            self.labels.append(l)
            self.widgets[text.lower()] = {}

        for i, stat in enumerate(STATS_NAMES, 1):
            l = QLabel(stat)
            self.labels.append(l)
            self.l.addWidget(l, i, 0)
            stat = stat.lower()
            for j in range(1, 4):
                widget = QU16()
                ty = self.STAT_TYPES[j - 1].lower()
                val = self.stats.__getattribute__(ty).__getattribute__(stat)
                widget.setValue(val)
                self.widgets[ty][stat] = widget
                self.l.addWidget(widget, i, j)

        for i, stat in enumerate(["hp", "mp"], 1):
            widget = QU16()
            val = self.healable.__getattribute__(stat)
            widget.setValue(val)
            self.widgets["healable"][stat] = widget
            self.l.addWidget(widget, i, 4)

        self.heal_button = QPushButton("Heal")
        self.heal_button.clicked.connect(self.on_heal)
        self.l.addWidget(self.heal_button, 8, 1)

    def on_heal(self):
        for stat in ["hp", "mp"]:
            value = self.widgets["current"][stat].value()
            self.widgets["healable"][stat].setValue(value)

    def apply_widget(self, ty: str, stat: str):
        if ty == "healable":
            def inner(value: int):
                self.healable.__setattr__(stat, value)
        else:
            def inner(value: int):
                self.stats.__getattribute__(ty).__setattr__(stat, value)
        return inner

    def on_apply_changes(self):
        for ty, v in self.widgets.items():
            for stat, widget in v.items():
                widget.update_if_modified(self.apply_widget(ty, stat))
