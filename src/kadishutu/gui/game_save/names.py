from kadishutu.core.game_save.player import NameEdit, NameManager
from typing import List, Tuple
from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget

from ..shared import AppliableWidget
from .shared import GameScreenMixin


OVERWRITTEN_WARN = "WARNING: This is overwritten with \"First name\" when saving"


class NameEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    NAMES = [
        "Save name", "First name", "Last name", "First name again",
        "Combined name"
    ]

    def __init__(self, names: NameManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.names = names
        self.widgets: List[Tuple[NameEdit, QLineEdit]] = []

        self.l = QVBoxLayout(self)

        for name in self.NAMES:
            label = QLabel(name, self)
            self.l.addWidget(label)
            name = name.lower().replace(" ", "_")
            if name == "save_name":
                label = QLabel(OVERWRITTEN_WARN, self)
                self.l.addWidget(label)
            editor: NameEdit = names.__getattribute__(name)
            box = QLineEdit(self)
            box.setMaxLength(editor.length)
            self.l.addWidget(box)
            self.widgets.append((editor, box))

    def stack_refresh(self):
        for editor, box in self.widgets:
            box.setText(editor.get())

    def on_apply_changes(self):
        for editor, box in self.widgets:
            if not box.isModified():
                continue
            editor.set(box.text())
            box.setModified(False)
