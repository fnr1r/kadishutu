from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSpinBox, QTabWidget, QVBoxLayout, QWidget,
)

from kadishutu.miracles import MiracleEditor, MiracleState

from .data.affinity import AFFINITY_MAP, Affinity
from .data.alignment import ALIGNMENT_DATA, AlignmentBit
from .data.demons import DEMON_ID_MAP, DEMON_NAME_MAP
from .data.element_icons import Element
from .data.items import (
    CONSUMABLES_RANGE, ESSENCES_RANGE, KEY_ITEMS_RANGE, RELICS_RANGE_1,
    RELICS_RANGE_2, Item, items_from
)
from .data.miracles import MIRACLE_DATA, Miracle
from .data.skills import SKILL_ID_MAP, SKILL_NAME_MAP
from .demons import (
    AFFINITY_NAMES, STATS_NAMES, AffinityEditor,
    DemonEditor, HealableEditor, PType, PotentialEditor, StatsEditor
)
from .dlc import DLCS, DlcBitflags
from .essences import EssenceEditor
from .file_handling import DecryptedSave
from .game import Difficulty, SaveEditor
from .gui_common import (
    QU16, QU32, QU8, SHIBOKEN_MAX, U16_MAX, AppliableWidget, MCheckBox,
    MComboBox, SaveScreenMixin, ScreenMixin, ModifiedMixin, hboxed
)
from .gui_icons import ICON_LOADER, DisabledError, print_icon_loading_error
from .items import ItemEditor
from .player import NameEdit, NameManager
from .skills import SkillEditor, SkillManager


OVERWRITTEN_WARN = "WARNING: This is overwritten with \"First name\" when saving"


class GameScreenMixin(ScreenMixin):
    def mixin(self):
        super().mixin()
        if not self.editor_widget_on_stack:
            return
        assert not hasattr(self, "save")
        self.save = self.game_save_editor.save

    @property
    def game_save_editor(self) -> "GameSaveEditorScreen":
        widget = self.some_save_editor_widget
        assert isinstance(widget, GameSaveEditorScreen)
        return widget


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


class DlcEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets: Dict[str, QCheckBox] = {}

        self.l = QGridLayout(self)

        for i, dlc in enumerate(DLCS.values()):
            label = QLabel(dlc)
            self.l.addWidget(label, i, 0)
            dlc_box = QCheckBox()
            self.l.addWidget(dlc_box, i, 1)
            self.widgets[dlc] = dlc_box

    def stack_refresh(self):
        dlcs = self.save.dlc.flags.get_flags()
        for name, dlc_box in self.widgets.items():
            dlc_box.setChecked(name in dlcs)

    def on_apply_changes(self):
        dlcs = [
            name
            for name, dlc_box in self.widgets.items()
            if dlc_box.isChecked()
        ]
        self.save.dlc.flags = DlcBitflags.from_flags(dlcs)


class StatEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    STAT_TYPES = ["Base", "Changes", "Current", "Healable"]

    def __init__(
        self,
        stats: StatsEditor,
        healable: HealableEditor,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.stats = stats
        self.healable = healable
        self.labels = []
        self.widgets: Dict[str, Dict[str, QU16]] = {}

        self.l = QGridLayout(self)

        for i in range(0, 4):
            text = self.STAT_TYPES[i]
            l = QLabel(text)
            self.l.addWidget(l, 0, i + 1)
            self.labels.append(l)
            self.widgets[text.lower()] = {}

        for i, stat in enumerate(STATS_NAMES, 1):
            l = QLabel(stat)
            self.labels.append(l)
            self.l.addWidget(l, i, 0)
            stat = stat.lower()
            for j in range(1, 4):
                widget = QU16()
                ty = self.STAT_TYPES[j - 1].lower()
                val = self.stats.__getattribute__(ty).__getattribute__(stat)
                widget.setValue(val)
                self.widgets[ty][stat] = widget
                self.l.addWidget(widget, i, j)

        for i, stat in enumerate(["hp", "mp"], 1):
            widget = QU16()
            val = self.healable.__getattribute__(stat)
            widget.setValue(val)
            self.widgets["healable"][stat] = widget
            self.l.addWidget(widget, i, 4)

        self.heal_button = QPushButton("Heal")
        self.heal_button.clicked.connect(self.on_heal)
        self.l.addWidget(self.heal_button, 8, 1)

    def on_heal(self):
        for stat in ["hp", "mp"]:
            value = self.widgets["current"][stat].value()
            self.widgets["healable"][stat].setValue(value)

    def apply_widget(self, ty: str, stat: str):
        if ty == "healable":
            def inner(value: int):
                self.healable.__setattr__(stat, value)
        else:
            def inner(value: int):
                self.stats.__getattribute__(ty).__setattr__(stat, value)
        return inner

    def on_apply_changes(self):
        for ty, v in self.widgets.items():
            for stat, widget in v.items():
                widget.update_if_modified(self.apply_widget(ty, stat))


class AbstractStrIntMap(QWidget, ModifiedMixin):
    def __init__(self, items: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedMixin.__init__(self)

        self.l = QHBoxLayout(self)
        self.l.setContentsMargins(0, 0, 0, 0)

        self.str_box = QComboBox()
        self.str_box.addItems(items)
        self.str_box.currentTextChanged.connect(self.str_changed)
        self.l.addWidget(self.str_box)

        self.int_box = QSpinBox()
        self.int_box.valueChanged.connect(self.int_changed)
        self.l.addWidget(self.int_box)

    def get_value(self) -> int:
        return self.int_box.value()

    @abstractmethod
    def refresh(self):
        raise NotImplementedError

    @abstractmethod
    def apply_changes(self):
        raise NotImplementedError

    @abstractmethod
    def int_to_str(self, value: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def str_to_int(self, value: str) -> int:
        raise NotImplementedError

    def int_changed(self, value: int):
        self.set_modified(True)
        self.str_box.setCurrentText(self.int_to_str(value))

    def str_changed(self, value: str):
        self.set_modified(True)
        self.int_box.setValue(self.str_to_int(value))


class SkillBox(AbstractStrIntMap, ModifiedMixin):
    NO_VALUE_INT = 0
    NO_VALUE_STR = "NONE"

    def __init__(self, skill: SkillEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.str_box.insertItem(0, self.NO_VALUE_STR)
        ModifiedMixin.__init__(self)
        self.skill = skill
        self.int_box.setMaximum(SHIBOKEN_MAX)

    def refresh(self):
        self.int_box.setValue(self.skill.id)
        if self.skill.id == self.NO_VALUE_INT:
            self.str_box.setCurrentIndex(0)
            return
        self.str_box.setCurrentText(self.skill.name)

    def apply_changes(self):
        if self.get_modified:
            self.skill.id = self.int_box.value()
            self.set_modified(False)

    def int_to_str(self, value: int) -> str:
        if value == self.NO_VALUE_INT:
            return self.NO_VALUE_STR
        return SKILL_ID_MAP[value].name

    def str_to_int(self, value: str) -> int:
        if value == self.NO_VALUE_STR:
            return self.NO_VALUE_INT
        return SKILL_NAME_MAP[value].id


class SkillEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(
        self,
        skills: SkillManager,
        innate_skill: SkillEditor,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.skills = skills
        self.widgets: List[Tuple[SkillBox, QU32]] = []

        self.l = QGridLayout(self)

        all_skills = list(SKILL_NAME_MAP.keys())

        for i in range(9):
            if i == 0:
                skill = innate_skill
                label = QLabel("Innate skill")
            else:
                skill = skills.slot(i - 1)
                label = QLabel(f"Skill {i}")
            self.l.addWidget(label, i, 0)
            skill_box = SkillBox(skill, all_skills)
            self.l.addWidget(skill_box, i, 2)
            mystery_box = QU32()
            self.l.addWidget(mystery_box, i, 4)
            icon = QLabel()
            self.l.addWidget(icon, i, 1)
            mp_cost = QLabel()
            self.l.addWidget(mp_cost, i, 3)
            if not i:
                mystery_box.hide()
                mp_cost.hide()
            cb = self.make_meta_refresh_callback(icon, mp_cost)
            skill_box.int_box.valueChanged.connect(cb)
            self.widgets.append((skill_box, mystery_box))

    def meta_refresh(
        self,
        skill_id: int,
        icon: QLabel,
        mp_cost: QLabel,
    ):
        if skill_id == SkillBox.NO_VALUE_INT:
            mp_cost.hide()
            icon.hide()
            return
        else:
            mp_cost.show()
            icon.show()
        skill_meta = SKILL_ID_MAP[skill_id]
        element = skill_meta.icon
        if element == Element.Passive:
            mp_cost.setText("MP cost: N/A")
        else:
            mp_cost.setText("MP cost: " + str(skill_meta.mp_cost))
        try:
            pak = ICON_LOADER.element_icon(element)
        except Exception as e:
            print_icon_loading_error(e, "Failed to load element icon:")
        else:
            pix = pak.pixmap.scaled(pak.size_div(2))
            icon.setFixedSize(pix.size())
            icon.setPixmap(pix)

    def make_meta_refresh_callback(
        self,
        icon: QLabel,
        mp_cost: QLabel,
    ):
        def inner(skill_id: int):
            return self.meta_refresh(skill_id, icon, mp_cost)
        return inner

    def stack_refresh(self):
        for i in range(9):
            skill_box, mystery_box = self.widgets[i]
            skill_box.refresh()
            skill = skill_box.skill
            mystery_box.setValue(skill._unknown)

    def on_apply_changes(self):
        for i in range(9):
            skill_box, mystery_box = self.widgets[i]
            skill_box.apply_changes()
            mystery_box.setattr_if_modified(skill_box.skill, "_unknown")


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
        self.potential_map: Dict[PType, QPotentialBox] = {}

        self.l = QGridLayout(self)

        for i, ptype in enumerate(PType):
            label = QLabel(ptype.name)
            self.l.addWidget(label, i, 1)
            potential_box = QPotentialBox()
            self.l.addWidget(potential_box, i, 2)
            self.potential_map[ptype] = potential_box
            try:
                if ptype.name == "_UNKNOWN":
                    elname = Element.Misc
                else:
                    elname = Element[ptype.name]
                pak = ICON_LOADER.element_icon(elname)
            except Exception as e:
                print_icon_loading_error(e, "Failed to load element icon:")
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel()
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                self.l.addWidget(icon, i, 0)

    def stack_refresh(self):
        for ptype, potential_box in self.potential_map.items():
            potential = self.potentials.get(ptype)
            potential_box.setValue(potential)

    def on_apply_changes(self):
        for ptype, potential_box in self.potential_map.items():
            potential_box.update_if_modified(
                lambda x: self.potentials.set(ptype, x)
            )


class PlayerEditorScreen(QWidget, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        for name, fun in [
            ("Names", lambda: NameEditorScreen(
                self.save.player.names
            )),
            ("Stats", lambda: StatEditorScreen(
                self.save.player.stats, self.save.player.healable
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.save.player.skills, self.save.player.innate_skill
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.save.player.affinities
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.save.player.potentials
            ))
        ]:
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.l.addWidget(button)

        self.l.addStretch()


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


class MiracleEditorWidget(QScrollArea, GameScreenMixin, AppliableWidget):
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
                print_icon_loading_error(e, "Failed to load element icon:")
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

    def on_apply_changes(self):
        for boxes in self.widgets:
            boxes.apply_changes()


class MiracleEditorScreen(QTabWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs: List[MiracleEditorWidget] = []

        for name, miracles in [
            ("In-Game", MIRACLE_DATA),
            ("Categories", []),
            ("Here", [])
        ]:
            widget = MiracleEditorWidget(miracles)
            self.tabs.append(widget)
            self.addTab(widget, name)

    def stack_refresh(self):
        for tab in self.tabs:
            tab.stack_refresh()

    def on_apply_changes(self):
        for tab in self.tabs:
            tab.on_apply_changes()


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
                pak = ICON_LOADER.element_icon(item.meta.icon)
            except Exception as e:
                print_icon_loading_error(e, "Failed to load element icon:")
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
                pak = ICON_LOADER.element_icon(Element.Pass)
            except Exception as e:
                print_icon_loading_error(e, "Failed to load element icon:")
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

    def on_apply_changes(self):
        for essence, _, owned_box, meta_box in self.essences:
            owned_box.setattr_if_modified(essence, "owned")
            meta_box.setattr_if_modified(essence, "metadata")


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


class SettingsEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout(self)
        self.difficulty = MComboBox()
        self.difficulty.addItems([
            difficulty.name
            for difficulty in Difficulty
        ])
        self.l.addLayout(hboxed(
            QLabel("Difficulty"), self.difficulty
        ))
        self.l.addStretch()

    def stack_refresh(self):
        self.difficulty.setCurrentText(self.save.difficulty.name)

    def _apply_difficulty(self, value: str):
        self.save.difficulty = Difficulty[value]

    def on_apply_changes(self):
        self.difficulty.update_if_modified(self._apply_difficulty)


class GameSaveEditorScreen(SaveScreenMixin, QWidget, AppliableWidget):
    path: Path
    raw_save: DecryptedSave
    save: SaveEditor
    modified: bool

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.save = SaveEditor(self.raw_save)

        self.l = QVBoxLayout(self)
        self.macca = QU32()
        self.l.addLayout(hboxed(QLabel("Macca"), self.macca))
        self.glory = QU32()
        self.l.addLayout(hboxed(QLabel("Glory"), self.glory))

        for name, cls in [
            ("DLC", DlcEditorScreen),
            ("Player", PlayerEditorScreen),
            ("Demons", DemonSelectorScreen),
            ("Miracles", MiracleEditorScreen),
            ("Items", ItemEditorScreen),
            ("Essences", EssenceEditorScreen),
            ("Alignment", AlignmentEditorScreen),
            ("Settings", SettingsEditorScreen),
        ]:
            widget = QPushButton(name)
            widget.clicked.connect(self.spawner(cls))
            self.l.addWidget(widget)

        self.l.addStretch()

    def stack_refresh(self):
        self.macca.setValue(self.save.macca)
        self.glory.setValue(self.save.glory)

    def on_apply_changes(self):
        self.macca.setattr_if_modified(self.save, "macca")
        self.glory.setattr_if_modified(self.save, "glory")
