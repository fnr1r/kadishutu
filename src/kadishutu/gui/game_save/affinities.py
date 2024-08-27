from kadishutu.core.game_save.affinities import (
    AILMENT_AFFINITY_NAMES, ELEMENTAL_AFFINITY_NAMES, AffinityManager,
)
from kadishutu.data.affinity import AFFINITY_MAP, Affinity
from kadishutu.data.element_icons import Element
from typing import Dict
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

from ..shared import AppliableWidget, MComboBox
from ..iconloader import ICON_LOADER, print_icon_loading_error
from .shared import GameScreenMixin


class AffinityEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, affinities: AffinityManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.affinities = affinities
        self.ail_aff_map: Dict[str, MComboBox] = {}
        self.elem_aff_map: Dict[str, MComboBox] = {}

        self.l = QGridLayout(self)
        cb_items = list(AFFINITY_MAP.keys())

        i = 0

        def make_wig(i: int, name: str):
            label = QLabel(name)
            self.l.addWidget(label, i, 1)
            affinity_box = MComboBox()
            affinity_box.addItems(cb_items)
            self.l.addWidget(affinity_box, i, 2)
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
            return affinity_box

        for name in ELEMENTAL_AFFINITY_NAMES:
            self.elem_aff_map[name.lower()] = make_wig(i, name)
            i += 1

        for name in AILMENT_AFFINITY_NAMES:
            self.ail_aff_map[name.lower()] = make_wig(i, name)
            i += 1

    def stack_refresh(self):
        ail_aff = self.affinities.ailment
        for name, affinity_box in self.ail_aff_map.items():
            affinity: Affinity = ail_aff.__getattribute__(name)
            affinity_box.setCurrentText(affinity.name)
        elem_aff = self.affinities.current_elemental
        for name, affinity_box in self.elem_aff_map.items():
            affinity: Affinity = elem_aff.__getattribute__(name)
            affinity_box.setCurrentText(affinity.name)

    def _upd(self, aff_editor, name: str):
        def inner(value: str):
            affinity = Affinity[value]
            aff_editor.__setattr__(name, affinity)
        return inner

    def on_apply_changes(self):
        ail_aff = self.affinities.ailment
        for name, affinity_box in self.ail_aff_map.items():
            affinity_box.update_if_modified(self._upd(ail_aff, name))
        elem_aff = self.affinities.current_elemental
        for name, affinity_box in self.elem_aff_map.items():
            affinity_box.update_if_modified(self._upd(elem_aff, name))
