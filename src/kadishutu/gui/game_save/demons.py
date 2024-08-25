from kadishutu.core.game_save.demons import DemonEditor
from kadishutu.data.demons import DEMON_ID_MAP, DEMON_NAME_MAP
from typing import List
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox,
    QVBoxLayout, QWidget,
)

from ..shared import (
    U16_MAX, AppliableWidget, ModifiedMixin, hboxed,
)
from ..iconloader import ICON_LOADER, DisabledError, print_icon_loading_error
from .affinities import AffinityEditorScreen
from .potentials import PotentialEditorScreen
from .shared import GameScreenMixin
from .skills import SkillEditorScreen
from .stats import StatEditorScreen


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


class DemonEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, demon: DemonEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demon = demon

        self.parent_layout = QHBoxLayout(self)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.side_panel_widget = QWidget(self)
        self.l = QVBoxLayout(self.side_panel_widget)
        self.parent_layout.addWidget(self.side_panel_widget)

        self.demon_idn_widget = DemonIdnWidget(
            demon,
            self.graphic_refresh,
            self.side_panel_widget
        )

        self.side_panel_widgets: List[QWidget] = [
            self.demon_idn_widget
        ]

        for name, fun in [
            ("Stats", lambda: StatEditorScreen(
                self.demon.stats, self.demon.healable
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.demon.skills, self.demon.innate_skill
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.demon.affinities
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.demon.potentials
            ))
        ]:
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.side_panel_widgets.append(button)

        for button in self.side_panel_widgets:
            self.l.addWidget(button)
        self.l.addStretch()

        self.demon_graphic = QLabel()
        self.parent_layout.addWidget(self.demon_graphic)

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


class DemonSelectorScreen(QWidget, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demons = self.save.demons
        self.widgets: List[QPushButton] = []

        self.l = QGridLayout(self)
        for demon_number in range(24):
            sel = QPushButton(self)
            sel.clicked.connect(self.demon_editor(demon_number))
            COLUMNS = 4
            (row, column) = divmod(demon_number, COLUMNS)
            self.l.addWidget(sel, row, column)
            self.widgets.append(sel)

    def demon_button_refresh(self, demon_number: int, button: QPushButton):
        demon = self.demons.in_slot(demon_number)
        if demon.demon_id == 0xffff:
            demon_txt = "None"
            button.setEnabled(False)
        else:
            try:
                demon_txt = demon.name
            except KeyError:
                demon_txt = f"Unknown ({demon.demon_id})"
            try:
                icon = ICON_LOADER.mini_character_icon(demon.meta.id)
            except Exception as e:
                print_icon_loading_error(e, "Failed to load demon icon:")
            else:
                button.setIcon(icon.icon)
                button.setIconSize(icon.size_div(2))
        button.setText(f"Demon {demon_number}: {demon_txt}")

    def stack_refresh(self):
        for demon_number, button in enumerate(self.widgets):
            self.demon_button_refresh(demon_number, button)

    def demon_editor(self, demon_number: int):
        demon = self.demons.in_slot(demon_number)
        return lambda: self.stack_add(
            DemonEditorScreen(demon, self)
        )
