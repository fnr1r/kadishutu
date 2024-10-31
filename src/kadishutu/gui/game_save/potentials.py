from typing import Dict

from PySide6.QtWidgets import QGridLayout, QLabel, QSpinBox, QWidget

from kadishutu.core.game_save.potentials import PotentialType, PotentialEditor
from kadishutu.data.element_icons import Element

from ..shared import AppliableWidget, ModifiedMixin
from ..iconloader import ICON_LOADER, handle_image_loading_error
from .shared import GameScreenMixin


class QPotentialBox(QSpinBox, ModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(-9)
        self.setMaximum(9)
        self.valueChanged.connect(self.flag_as_modified)

    def get_value(self) -> int:
        return self.value()


class PotentialEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, potentials: PotentialEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.potentials = potentials
        self.potential_map: Dict[PotentialType, QPotentialBox] = {}

        self.l = QGridLayout(self)

        for i, ptype in enumerate(PotentialType):
            label = QLabel(ptype.name)
            self.l.addWidget(label, i, 1)
            potential_box = QPotentialBox()
            self.l.addWidget(potential_box, i, 2)
            self.potential_map[ptype] = potential_box
            if ptype.name == "_UNKNOWN":
                elname = Element.Misc
            else:
                elname = Element[ptype.name]
            try:
                pak = ICON_LOADER.element_icon(elname)
            except Exception as e:
                handle_image_loading_error(e, "element", elname)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                self.l.addWidget(icon, i, 0)

    def stack_refresh(self):
        for ptype, potential_box in self.potential_map.items():
            potential = self.potentials.read(ptype)
            potential_box.setValue(potential)

    def on_apply_changes(self):
        for ptype, potential_box in self.potential_map.items():
            potential_box.update_if_modified(
                lambda x: self.potentials.write(ptype, x)
            )
