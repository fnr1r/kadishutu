from kadishutu.core.game_save.demons import DEMON_TABLE_SIZE, DemonEditor
from kadishutu.data.demons import DEMON_ID_MAP, DEMON_NAME_MAP
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QMenu, QLabel, QPushButton, QSpinBox,
    QVBoxLayout, QWidget,
)

from ..shared import (
    U16_MAX, AppliableWidget, ModifiedMixin, hboxed,
)
from ..iconloader import ICON_LOADER, DisabledError, print_icon_loading_error
from .demonlike import DemonLikeEditorScreen
from .shared import GameScreenMixin

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


class DemonIdnWidget(QWidget, ModifiedMixin):
    def __init__(self, demon: DemonEditor, graphic_refresh, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedMixin.__init__(self)
        self.demon = demon.meta
        self.graphic_refresh = graphic_refresh

        self.l = QVBoxLayout(self)
        self.l.setContentsMargins(0, 0, 0, 0)

        self.id_label = QLabel("ID:")
        self.id_box = QSpinBox()
        self.id_box.setMaximum(U16_MAX)
        self.id_box.setValue(demon.demon_id)
        self.id_box.valueChanged.connect(self.id_changed)
        self.l.addLayout(hboxed(self.id_label, self.id_box))

        self.name_label = QLabel("Name:")
        self.name_box = QComboBox()
        self.name_box.addItems(list(DEMON_NAME_MAP.keys()))
        self.name_box.setCurrentText(demon.name)
        self.name_box.currentTextChanged.connect(self.name_changed)
        self.l.addLayout(hboxed(self.name_label, self.name_box))

    def get_value(self) -> int:
        return self.demon.id

    def id_changed(self, id: int):
        self.set_modified(True)
        try:
            self.demon = DEMON_ID_MAP[id]
        except KeyError:
            return
        self.name_box.blockSignals(True)
        self.name_box.setCurrentText(self.demon.name)
        self.name_box.blockSignals(False)
        self.graphic_refresh()

    def name_changed(self, name: str):
        self.set_modified(True)
        self.demon = DEMON_NAME_MAP[name]
        self.id_box.blockSignals(True)
        self.id_box.setValue(self.demon.id)
        self.id_box.blockSignals(False)
        self.graphic_refresh()


class DemonEditorScreen(DemonLikeEditorScreen, AppliableWidget):
    demon: DemonEditor

    def __init__(self, demon: DemonEditor, *args, **kwargs):
        super().__init__(demon, *args, **kwargs)
        self.l = QHBoxLayout(self)
        self.l.addLayout(self.dl_layout)

        self.demon_idn_widget = DemonIdnWidget(
            demon,
            self.graphic_refresh,
        )
        self.dl_layout.insertWidget(0, self.demon_idn_widget)

        self.demon_graphic = QLabel()
        self.l.addWidget(self.demon_graphic)

    def graphic_refresh(self):
        try:
            id = self.demon_idn_widget.demon.id
            icon = ICON_LOADER.loading_character_icon(id)
        except Exception as e:
            print_icon_loading_error(e, "Failed to demon grapic:")
            if isinstance(e, FileNotFoundError) or isinstance(e, DisabledError):
                self.demon_graphic.hide()
        else:
            size = icon.size_div(2)
            self.demon_graphic_pix = icon.pixmap.scaled(size)
            self.demon_graphic.setPixmap(self.demon_graphic_pix)
            self.demon_graphic.setFixedSize(size)
            self.demon_graphic.show()

    def stack_refresh(self):
        self.graphic_refresh()

    def on_apply_changes(self):
        self.demon_idn_widget.setattr_if_modified(self.demon, "demon_id")


CIDS = Callable[[int, DemonEditor], "SupportsRichComparison"]


class DemonSelectorScreen(QWidget, GameScreenMixin, AppliableWidget):
    _new_demon_order: Optional[List[int]] = None
    NO_DEMON = 0xff

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demons = self.save.demons
        self.team = team = self.save.team
        self.widgets: List[QPushButton] = []

        self.l = QGridLayout(self)
        for i, demon_number in enumerate(team.demon_order):
            sel = QPushButton(self)
            sel.clicked.connect(self.demon_editor(demon_number))
            self.l.addWidget(sel, *divmod(i, 4))
            self.widgets.append(sel)

        self.sort_menu = sort_menu = QMenu("Sort", self)
        sort_types_list: List[Tuple[str, Optional[CIDS]]] = [
            ("by slot", lambda x, _: x),
            ("by demon ID", lambda _, x: x.demon_id),
            ("separator", None),
            ("by level", lambda _, x: -x.level),
            ("by max hp", lambda _, x: -x.stats.current.hp),
            ("by max mp", lambda _, x: -x.stats.current.mp),
            ("by name (alphabetically)", lambda _, x: x.meta.name),
        ]
        for name, fun in sort_types_list:
            if fun is None:
                sort_menu.addSeparator()
                continue
            def a(fun: CIDS):
                return lambda: self.sort_with_fun(fun)
            sort_menu.addAction(name).triggered.connect(a(fun))
        self.sort_button = QPushButton("Sort")
        self.sort_button.setMenu(self.sort_menu)
        self.l.addWidget(self.sort_button, 8, 0)

    @property
    def demon_order(self) -> List[int]:
        if self._new_demon_order:
            return self._new_demon_order
        return self.team.demon_order

    def sort_with_fun(self, fun: CIDS):
        demons = self.demons
        demon_order = self.demon_order
        while demon_order[-1] == self.NO_DEMON:
            demon_order.pop()
        demon_order.sort(key=lambda x: fun(x, demons.in_slot(x)))
        for _ in range(len(demon_order), DEMON_TABLE_SIZE):
            demon_order.append(self.NO_DEMON)
        self._new_demon_order = demon_order
        self.stack_refresh()

    def demon_button_refresh(self, demon_number: int, button: QPushButton):
        if demon_number == self.NO_DEMON:
            button.setEnabled(False)
            button.setText("Empty")
            button.setIcon(ICON_LOADER.no_icon)
            return
        button.setEnabled(True)
        demon = self.demons.in_slot(demon_number)
        try:
            demon_txt = demon.name
        except KeyError:
            demon_txt = f"Unknown ({demon.demon_id})"
        button.setText(f"Demon {demon_number}: {demon_txt}")
        try:
            icon = ICON_LOADER.mini_character_icon(demon.meta.id)
        except Exception as e:
            print_icon_loading_error(e, "Failed to load demon icon")
        else:
            button.setIcon(icon.icon)
            button.setIconSize(icon.size_div(2))

    def stack_refresh(self):
        for demon_number, button in zip(self.demon_order, self.widgets):
            self.demon_button_refresh(demon_number, button)

    def on_apply_changes(self):
        if self._new_demon_order is not None:
            self.team.demon_order = self._new_demon_order
            self._new_demon_order = None

    def demon_editor(self, demon_number: int):
        demon = self.demons.in_slot(demon_number)
        return lambda: self.stack_add(
            DemonEditorScreen(demon, self)
        )
