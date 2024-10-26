from kadishutu.core.game_save.essences import EssenceEditor, EssenceMetadata
from kadishutu.data.element_icons import Element
from kadishutu.data.items import ESSENCES_RANGE, items_from
from typing import List, Tuple
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QWidget

from ..shared import QU16, AppliableWidget, MCheckBox
from ..iconloader import ICON_LOADER, handle_image_loading_error
from .shared import GameScreenMixin


class EssenceEditorScreen(QScrollArea, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.essences: List[Tuple[EssenceEditor, QLabel, MCheckBox, QU16]] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QGridLayout(self.inner)

        items = items_from(ESSENCES_RANGE)

        for i, meta in enumerate(items):
            essence = self.save.essences.from_meta(meta)
            assert isinstance(essence, EssenceEditor)
            label = QLabel(essence.name)
            self.l.addWidget(label, i, 1)
            try:
                element = Element.Pass
                pak = ICON_LOADER.element_icon(element)
            except Exception as e:
                handle_image_loading_error(e, "element", element)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                self.l.addWidget(icon, i, 0)
            owned_box = MCheckBox()
            self.l.addWidget(owned_box, i, 2)
            meta_box = QU16()
            self.l.addWidget(meta_box, i, 3)
            self.essences.append((essence, label, owned_box, meta_box))

    def stack_refresh(self):
        for essence, _, owned_box, meta_box in self.essences:
            owned_box.setChecked(essence.owned)
            meta_box.setValue(essence.metadata)
            meta_box.set_modified(False)

    def on_apply_changes(self):
        for essence, _, owned_box, meta_box in self.essences:
            owned_box.setattr_if_modified(essence, "owned")
            def ess_set(essence_val: int):
                essence.metadata = EssenceMetadata(essence_val)
            meta_box.update_if_modified(ess_set)
