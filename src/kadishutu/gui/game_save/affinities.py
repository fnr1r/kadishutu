from kadishutu.core.game_save.demons import AFFINITY_NAMES, AffinityEditor
from kadishutu.data.affinity import AFFINITY_MAP, Affinity
from kadishutu.data.element_icons import Element
from typing import Dict
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

from ..shared import AppliableWidget, MComboBox
from ..iconloader import ICON_LOADER, print_icon_loading_error
from .shared import GameScreenMixin


class AffinityEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, affinities: AffinityEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.affinities = affinities
        self.aff_map: Dict[str, MComboBox] = {}

        self.l = QGridLayout(self)
        cb_items = list(AFFINITY_MAP.keys())

        for i, name in enumerate(AFFINITY_NAMES):
            label = QLabel(name)
            self.l.addWidget(label, i, 1)
            affinity_box = MComboBox()
            affinity_box.addItems(cb_items)
            self.l.addWidget(affinity_box, i, 2)
            self.aff_map[name.lower()] = affinity_box
            try:
                pak = ICON_LOADER.element_icon(Element[name])
            except Exception as e:
                print_icon_loading_error(e, "Failed to load element icon:")
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                self.l.addWidget(icon, i, 0)

    def stack_refresh(self):
        for name, affinity_box in self.aff_map.items():
            affinity: Affinity = self.affinities.__getattribute__(name)
            affinity_box.setCurrentText(affinity.name)

    def _upd(self, name: str):
        def inner(value: str):
            affinity = Affinity[value]
            self.affinities.__setattr__(name, affinity)
        return inner

    def on_apply_changes(self):
        for name, affinity_box in self.aff_map.items():
            affinity_box.update_if_modified(self._upd(name))
