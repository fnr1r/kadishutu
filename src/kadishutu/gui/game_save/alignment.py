from dataclasses import dataclass
from kadishutu.data.alignment import ALIGNMENT_DATA, AlignmentBit
from typing import Dict, List, Tuple
from PySide6.QtWidgets import (
    QCheckBox, QGridLayout, QLabel, QScrollArea, QTabWidget, QWidget,
)

from ..shared import AppliableWidget
from .shared import GameScreenMixin


@dataclass
class AlignmentPacked:
    outer: QScrollArea
    inner: QWidget
    layout: QGridLayout
    i: int

    @classmethod
    def from_parent(cls, parent: QTabWidget, name: str):
        outer = QScrollArea(parent)
        outer.setWidgetResizable(True)
        inner = QWidget(outer)
        outer.setWidget(inner)
        layout = QGridLayout(inner)
        inner.setLayout(layout)
        parent.addTab(outer, name)
        return cls(outer, inner, layout, 0)

    def add_widgets(self, *args: QWidget):
        for i, widget in enumerate(args):
            widget.setParent(self.inner)
            self.layout.addWidget(widget, self.i, i)
        self.i += 1


class AlignmentEditorScreen(QTabWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignment = self.save.alignment
        self.tabmap: Dict[str, AlignmentPacked] = {}
        self.checkboxmap: Dict[int, QCheckBox] = {}

        for name in ["Main story", "Side quests"]:
            nameq = name.lower().replace(" ", "_")
            self.tabmap[nameq] = AlignmentPacked.from_parent(self, name)

        self.flat_data: List[Tuple[int, AlignmentBit]] = []

        for byte in ALIGNMENT_DATA:
            for bit in byte.bits:
                self.flat_data.append((byte.offset, bit))

        for offset, bit in self.flat_data:
            packed = list(self.tabmap.values())[int(bit.side_quest is None)]
            packed.add_widgets(
                QLabel(f"Offset: 0x{offset:04}"),
                QLabel("Bit: " + str(bit.bit))
            )
            packed.add_widgets(
                QLabel("Alignment: " + bit.alignment.capitalize()),
                QLabel("Place: " + bit.place)
            )
            for text in bit.text:
                packed.add_widgets(QLabel(text))
            box = QCheckBox(packed.inner)
            packed.layout.addWidget(box, packed.i - 1, 1)
            self.checkboxmap[offset * 8 + bit.bit] = box

    def stack_refresh(self):
        for byte in ALIGNMENT_DATA:
            byte_editor = self.alignment.at_offset(byte.offset)
            for bit in byte.bits:
                box = self.checkboxmap[byte.offset * 8 + bit.bit]
                box.setChecked(byte_editor.get_flag(bit.bit))

    def on_apply_changes(self):
        for byte in ALIGNMENT_DATA:
            byte_editor = self.alignment.at_offset(byte.offset)
            for bit in byte.bits:
                box = self.checkboxmap[byte.offset * 8 + bit.bit]
                byte_editor.set_flag(bit.bit, box.isChecked())
