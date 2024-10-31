from typing import List, Tuple

from PySide6.QtWidgets import (
    QGridLayout, QLabel, QScrollArea, QTabWidget, QWidget,
)

from kadishutu.core.game_save.items import ItemEditor
from kadishutu.data.items import (
    CONSUMABLES_RANGE, KEY_ITEMS_RANGE, RELICS_RANGE_1, RELICS_RANGE_2, Item,
    items_from,
)

from ..shared import QU8, AppliableWidget
from ..iconloader import ICON_LOADER, handle_image_loading_error
from .shared import GameScreenMixin


class ItemEditorWidget(QScrollArea, GameScreenMixin, AppliableWidget):
    def __init__(self, items: List[Item], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: List[Tuple[ItemEditor, QLabel, QU8]] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QGridLayout(self.inner)

        for i, meta in enumerate(items):
            item = self.save.items.from_meta(meta)
            label = QLabel(item.name)
            desc = item.meta.desc
            if desc is not None:
                label.setToolTip(desc)
            self.l.addWidget(label, i, 1)
            try:
                element = item.meta.icon
                pak = ICON_LOADER.element_icon(element)
            except Exception as e:
                handle_image_loading_error(e, "element", element)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                if desc is not None:
                    icon.setToolTip(desc)
                self.l.addWidget(icon, i, 0)
            limit_label = QLabel("Limit: " + str(item.limit))
            if desc is not None:
                limit_label.setToolTip(desc)
            self.l.addWidget(limit_label, i, 2)
            amount_box = QU8()
            if desc is not None:
                amount_box.setToolTip(desc)
            self.l.addWidget(amount_box, i, 3)
            self.items.append((item, label, amount_box))

    def stack_refresh(self):
        for item, _, amount_box in self.items:
            amount_box.setValue(item.amount)

    def on_apply_changes(self):
        for item, _, amount_box in self.items:
            amount_box.setattr_if_modified(item, "amount")


class ItemEditorScreen(QTabWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs: List[ItemEditorWidget] = []

        for name, item_ranges in [
            ("Consumables", [CONSUMABLES_RANGE]),
            ("Relics", [RELICS_RANGE_1, RELICS_RANGE_2]),
            ("Key Items", [KEY_ITEMS_RANGE])
        ]:
            items = items_from(*item_ranges)
            widget = ItemEditorWidget(items)
            self.tabs.append(widget)
            self.addTab(widget, name)

    def stack_refresh(self):
        for tab in self.tabs:
            tab.stack_refresh()

    def on_apply_changes(self):
        for tab in self.tabs:
            tab.on_apply_changes()
