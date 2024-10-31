from typing import List, Tuple

from PySide6.QtWidgets import (
    QGridLayout, QHBoxLayout, QLabel, QListWidget, QScrollArea, QTabWidget,
    QVBoxLayout, QWidget,
)

from kadishutu.core.game_save.miracles import MiracleEditor, MiracleState
from kadishutu.core.game_save.miracle_unlocks import MiracleUnlockEditor
from kadishutu.data.element_icons import Element
from kadishutu.data.miracles import (
    MIRACLE_DATA, MIRACLES, Miracle, MiracleCategory,
)
from kadishutu.data.miracle_unlocks import MIRACLE_UNLOCKS

from ..shared import AppliableWidget, MCheckBox
from ..iconloader import ICON_LOADER, handle_image_loading_error
from .shared import GameScreenMixin


class MiracleCheckboxes:
    def __init__(self, miracle: MiracleEditor, i: int, layout: QGridLayout):
        self.miracle = miracle

        self.seen_box = MCheckBox()
        self.seen_box.clicked.connect(self.boxes_refresh)
        layout.addWidget(self.seen_box, i, 2)
        self.bought_box = MCheckBox()
        self.bought_box.clicked.connect(self.boxes_refresh)
        layout.addWidget(self.bought_box, i, 3)
        self.enabled_box = MCheckBox()
        #toggleable = miracle.meta.toggleable
        #if toggleable is not None and not toggleable:
        #    self.enabled_box.hide()
        layout.addWidget(self.enabled_box, i, 4)

    @property
    def boxes(self):
        return [self.bought_box,self.seen_box,self.enabled_box]

    def boxes_refresh(self):
        seen = self.seen_box.isChecked()
        bought = self.bought_box.isChecked()
        self.bought_box.setEnabled(seen)
        self.enabled_box.setEnabled(seen & bought)

    def refresh(self):
        state = self.miracle.state
        for state_i, box in zip(MiracleState.all(), self.boxes):
            value = bool(state & state_i)
            box.setChecked(value)
            box.set_modified(False)
        self.boxes_refresh()

    def apply_changes(self):
        if not (self.seen_box.get_modified() or
            self.bought_box.get_modified() or
            self.enabled_box.get_modified()):
            return
        state = MiracleState.none()
        for state_i, box in zip(MiracleState.all(), self.boxes):
            if box.isEnabled() & box.isChecked():
                state |= state_i
            box.set_modified(False)
        self.miracle.state = state


class MiracleEditorWidget(QScrollArea, GameScreenMixin):
    def __init__(self, miracles: List[Miracle], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets: List[MiracleCheckboxes] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QGridLayout(self.inner)

        self.l.addWidget(QLabel("Seen"), 0, 2)
        self.l.addWidget(QLabel("Bought"), 0, 3)
        self.l.addWidget(QLabel("Enabled"), 0, 4)

        def try_to_sort_by_ord_id(mir: Miracle):
            if mir.order_id is not None:
                return mir.order_id
            else:
                return mir.id

        miracles.sort(key=try_to_sort_by_ord_id)

        for i, meta in enumerate(miracles, 1):
            miracle = self.save.miracles.from_meta(meta)
            label = QLabel(miracle.name)
            desc = miracle.meta.desc
            if desc is not None:
                label.setToolTip(desc)
            self.l.addWidget(label, i, 1)
            try:
                pak = ICON_LOADER.element_icon(Element.PressTurn)
            except Exception as e:
                handle_image_loading_error(e, "element", icon)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                if desc is not None:
                    icon.setToolTip(desc)
                self.l.addWidget(icon, i, 0)
            boxes = MiracleCheckboxes(miracle, i, self.l)
            self.widgets.append(boxes)

    def stack_refresh(self):
        for boxes in self.widgets:
            boxes.refresh()

    def apply_changes(self):
        for boxes in self.widgets:
            boxes.apply_changes()


class MiracleUnlockerWidget(QScrollArea, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unlocks = self.save.miracle_unlocks
        self.widgets: List[Tuple[MiracleUnlockEditor, MCheckBox]] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QVBoxLayout(self.inner)

        for i, unlock in enumerate(MIRACLE_UNLOCKS):
            editor = self.unlocks.from_meta(unlock)
            layout = QVBoxLayout()
            sublayout = QHBoxLayout()
            layout.addLayout(sublayout)
            unlock_box = MCheckBox()
            sublayout.addWidget(unlock_box)
            label = QLabel(unlock.name)
            sublayout.addWidget(label)
            lst = QListWidget()
            for i in unlock.miracles:
                lst.addItem(i)
            layout.addWidget(lst)
            self.l.addLayout(layout)
            self.widgets.append((editor, unlock_box))

        sublayout = QHBoxLayout()
        self.satan_unlock_box = MCheckBox()
        sublayout.addWidget(self.satan_unlock_box)
        label = QLabel("Extra: Satan beaten flag")
        sublayout.addWidget(label)
        layout.insertLayout(1, sublayout)

    def stack_refresh(self):
        for editor, unlock_box in self.widgets:
            unlock_box.setChecked(editor.state)
        self.satan_unlock_box.setChecked(self.unlocks.extras.satan_beaten)

    def apply_changes(self):
        for editor, unlock_box in self.widgets:
            unlock_box.setattr_if_modified(editor, "state")
        self.satan_unlock_box.setattr_if_modified(
            self.unlocks.extras, "satan_beaten"
        )


class MiracleEditorScreen(QTabWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.miracle_tabs: List[MiracleEditorWidget] = []

        if MIRACLE_DATA:
            categorized_miracles = [
                (i, [
                    j
                    for j in MIRACLES
                    if j.category == i
                ])
                for i in MiracleCategory
                if i != MiracleCategory.NoCategory
            ]

            for category, miracles in categorized_miracles:
                widget = MiracleEditorWidget(miracles)
                self.miracle_tabs.append(widget)
                self.addTab(widget, category.name)
        else:
            widget = MiracleEditorWidget(MIRACLES)
            self.miracle_tabs.append(widget)
            self.addTab(widget, "Miracles (uncategorized)")

        self.unlocks_widget = MiracleUnlockerWidget()
        self.addTab(self.unlocks_widget, "★Unlocks")

    def stack_refresh(self):
        for tab in self.miracle_tabs:
            tab.stack_refresh()
        self.unlocks_widget.stack_refresh()

    def on_apply_changes(self):
        for tab in self.miracle_tabs:
            tab.apply_changes()
        self.unlocks_widget.apply_changes()
