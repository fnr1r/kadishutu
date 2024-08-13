from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSpinBox, QTabWidget, QVBoxLayout, QWidget,
)

from .data.alignment import ALIGNMENT_DATA, AlignmentBit
from .data.demons import DEMON_ID_MAP, DEMON_NAME_MAP
from .data.element_icons import Element
from .data.items import (
    CONSUMABLES_RANGE, KEY_ITEMS_RANGE, RELICS_RANGE_1, RELICS_RANGE_2,
    Item, items_from
)
from .data.skills import SKILL_ID_MAP, SKILL_NAME_MAP
from .demons import (
    AFFINITY_MAP, AFFINITY_NAMES, STATS_NAMES, Affinity, AffinityEditor,
    DemonEditor, HealableEditor, PType, PotentialEditor, StatsEditor
)
from .dlc import DLCS, DlcBitflags
from .file_handling import DecryptedSave
from .game import Difficulty, SaveEditor
from .gui_common import (
    QU16, QU32, QU8, U16_MAX, AppliableWidget, MComboBox, SaveScreenMixin,
    ScreenMixin, ModifiedMixin, hboxed
)
from .gui_icons import ICON_LOADER
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
        self.namelist: List[Tuple[NameEdit, QLineEdit]] = []

        self.setLayout(QVBoxLayout())

        for name in self.NAMES:
            label = QLabel(name, self)
            self.layout().addWidget(label)
            name = name.lower().replace(" ", "_")
            if name == "save_name":
                label = QLabel(OVERWRITTEN_WARN, self)
                self.layout().addWidget(label)
            editor: NameEdit = names.__getattribute__(name)
            box = QLineEdit(self)
            box.setMaxLength(editor.length)
            self.layout().addWidget(box)
            self.namelist.append((editor, box))

    def stack_refresh(self):
        for editor, box in self.namelist:
            box.setText(editor.get())

    def on_apply_changes(self):
        for editor, box in self.namelist:
            if not box.isModified():
                continue
            editor.set(box.text())
            box.setModified(False)


class DlcEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dlcmap: Dict[str, QCheckBox] = {}

        self.l = QGridLayout()
        self.setLayout(self.l)

        for i, dlc in enumerate(DLCS.values()):
            label = QLabel(dlc, self)
            self.l.addWidget(label, i, 0)
            dlc_box = QCheckBox(self)
            self.l.addWidget(dlc_box, i, 1)
            self.dlcmap[dlc] = dlc_box

    def stack_refresh(self):
        dlcs = self.save.dlc.flags.get_flags()
        for name, dlc_box in self.dlcmap.items():
            dlc_box.setChecked(name in dlcs)

    def on_apply_changes(self):
        dlcs = [
            name
            for name, dlc_box in self.dlcmap.items()
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
        self.l = QGridLayout()
        self.setLayout(self.l)
        for i in range(0, 4):
            text = self.STAT_TYPES[i]
            l = QLabel(text, self)
            self.l.addWidget(l, 0, i + 1)
            self.labels.append(l)
            self.widgets[text.lower()] = {}
        for i, stat in enumerate(STATS_NAMES, 1):
            l = QLabel(stat, self)
            self.labels.append(l)
            self.l.addWidget(l, i, 0)
            stat = stat.lower()
            for j in range(1, 4):
                widget = QU16(self)
                ty = self.STAT_TYPES[j - 1].lower()
                val = self.stats.__getattribute__(ty).__getattribute__(stat)
                widget.setValue(val)
                self.widgets[ty][stat] = widget
                self.l.addWidget(widget, i, j)
        for i, stat in enumerate(["hp", "mp"], 1):
            widget = QU16(self)
            val = self.healable.__getattribute__(stat)
            widget.setValue(val)
            self.widgets["healable"][stat] = widget
            self.l.addWidget(widget, i, 4)

        self.heal_button = QPushButton("Heal", self)
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
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.str_box = QComboBox(self)
        self.str_box.addItems(items)
        self.str_box.currentTextChanged.connect(self.str_changed)
        self.layout().addWidget(self.str_box)
        self.int_box = QSpinBox(self)
        self.int_box.valueChanged.connect(self.int_changed)
        self.layout().addWidget(self.int_box)

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
    def __init__(self, skill: SkillEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedMixin.__init__(self)
        self.skill = skill
        self.int_box.setMaximum(U16_MAX)

    def refresh(self):
        self.int_box.setValue(self.skill.id)
        self.str_box.setCurrentText(self.skill.name)

    def apply_changes(self):
        if self.get_modified:
            self.skill.id = self.int_box.value()
            self.set_modified(False)

    def int_to_str(self, value: int) -> str:
        return SKILL_ID_MAP[value].name

    def str_to_int(self, value: str) -> int:
        return SKILL_NAME_MAP[value].id


class SkillEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, skills: SkillManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.widgets: List[Tuple[SkillBox, QU16]] = []

        for i in range(8):
            skill = skills.slot(i)
            label = QLabel(f"Skill {i + 1}", self)
            skill_box = SkillBox(skill, list(SKILL_NAME_MAP.keys()), self)
            mystery_box = QU16(self)
            self.l.addLayout(hboxed(label, skill_box, mystery_box))
            self.widgets.append((skill_box, mystery_box))

        self.l.addStretch()

    def stack_refresh(self):
        for i in range(8):
            skill_box, mystery_box = self.widgets[i]
            skill_box.refresh()
            skill = skill_box.skill
            mystery_box.setValue(skill._unknown)

    def on_apply_changes(self):
        for i in range(8):
            skill_box, mystery_box = self.widgets[i]
            skill_box.apply_changes()
            mystery_box.setattr_if_modified(skill_box.skill, "_unknown")


class AffinityEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, affinities: AffinityEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.affinities = affinities
        self.aff_map: Dict[str, MComboBox] = {}

        self.l = QGridLayout(self)
        self.setLayout(self.l)
        cb_items = list(AFFINITY_MAP.keys())

        for i, name in enumerate(AFFINITY_NAMES):
            label = QLabel(name)
            self.l.addWidget(label, i, 1)
            affinity_box = MComboBox(self)
            affinity_box.addItems(cb_items)
            self.l.addWidget(affinity_box, i, 2)
            self.aff_map[name.lower()] = affinity_box
            try:
                pak = ICON_LOADER.element_icon(Element[name])
            except Exception as e:
                print("Failed to load element icon:", e)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel(self)
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
        self.setLayout(self.l)

        for i, ptype in enumerate(PType):
            label = QLabel(ptype.name)
            self.l.addWidget(label, i, 1)
            potential_box = QPotentialBox(self)
            self.l.addWidget(potential_box, i, 2)
            self.potential_map[ptype] = potential_box
            try:
                if ptype.name == "_UNKNOWN":
                    elname = Element.Misc
                else:
                    elname = Element[ptype.name]
                pak = ICON_LOADER.element_icon(elname)
            except Exception as e:
                print("Failed to load element icon:", e)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel(self)
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
        self.buttons = []

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        for name, fun in [
            ("Names", lambda: NameEditorScreen(
                self.save.player.names, self
            )),
            ("Stats", lambda: StatEditorScreen(
                self.save.player.stats, self.save.player.healable, self
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.save.player.skills, self
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.save.player.affinities, self
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.save.player.potentials, self
            ))
        ]:
            button = QPushButton(name, self)
            button.clicked.connect(self.spawner(fun))
            self.l.addWidget(button)
            self.buttons.append(button)

        self.l.addStretch()


class DemonIdnWidget(QWidget, ModifiedMixin):
    def __init__(self, demon: DemonEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedMixin.__init__(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.id_label = QLabel("ID:", self)
        self.id_box = QSpinBox(self)
        self.id_box.setMaximum(U16_MAX)
        self.id_box.setValue(demon.demon_id)
        self.id_box.valueChanged.connect(self.id_changed)
        self.l.addLayout(hboxed(self.id_label, self.id_box))

        self.name_label = QLabel("Name:", self)
        self.name_box = QComboBox(self)
        self.name_box.addItems(list(DEMON_NAME_MAP.keys()))
        self.name_box.setCurrentText(demon.name)
        self.name_box.currentTextChanged.connect(self.name_changed)
        self.l.addLayout(hboxed(self.name_label, self.name_box))

    def get_value(self) -> int:
        return self.id_box.value()

    def id_changed(self, id: int):
        self.set_modified(True)
        try:
            self.name_box.setCurrentText(DEMON_ID_MAP[id]["name"])
        except KeyError:
            pass

    def name_changed(self, name: str):
        self.set_modified(True)
        self.id_box.setValue(DEMON_NAME_MAP[name]["id"])


class DemonEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, demon: DemonEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demon = demon

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.side_panel_widget = QWidget(self)
        self.side_panel_layout = QVBoxLayout()
        self.side_panel_widget.setLayout(self.side_panel_layout)
        self.layout().addWidget(self.side_panel_widget)

        self.demon_idn_widget = DemonIdnWidget(demon, self.side_panel_widget)

        self.side_panel_widgets: List[QWidget] = [
            self.demon_idn_widget
        ]

        for name, fun in [
            ("Stats", lambda: StatEditorScreen(
                self.demon.stats, self.demon.healable, self
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.demon.skills, self
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.demon.affinities, self
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.demon.potentials, self
            ))
        ]:
            button = QPushButton(name, self.side_panel_widget)
            button.clicked.connect(self.spawner(fun))
            self.side_panel_widgets.append(button)

        for button in self.side_panel_widgets:
            self.side_panel_layout.addWidget(button)
        self.side_panel_layout.addStretch()

        self.demon_graphic = QLabel(self)
        self.layout().addWidget(self.demon_graphic)

    def stack_refresh(self):
        try:
            icon = ICON_LOADER.loading_character_icon(self.demon.demon_id)
        except FileNotFoundError:
            self.demon_graphic.hide()
        else:
            size = icon.size_div(2)
            self.demon_graphic_pix = icon.pixmap.scaled(size)
            self.demon_graphic.setPixmap(self.demon_graphic_pix)
            self.demon_graphic.setFixedSize(size)
            self.demon_graphic.show()

    def on_apply_changes(self):
        self.demon_idn_widget.setattr_if_modified(self.demon, "demon_id")


class DemonSelectorScreen(QWidget, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QGridLayout()
        self.setLayout(self.l)
        self.demons: List[QPushButton] = []
        for demon_number in range(24):
            sel = QPushButton(self)
            sel.clicked.connect(self.demon_editor(demon_number))
            COLUMNS = 4
            row = demon_number // COLUMNS
            column = demon_number % COLUMNS
            self.l.addWidget(sel, row, column)
            self.demons.append(sel)

    def demon_button_refresh(self, demon_number: int, button: QPushButton):
        demon = self.save.demon(demon_number)
        if demon.demon_id == 0xffff:
            demon_txt = "None"
            button.setEnabled(False)
        else:
            try:
                demon_txt = demon.name
            except KeyError:
                demon_txt = f"Unknown ({demon.demon_id})"
            try:
                icon = ICON_LOADER.mini_character_icon(demon.demon_id)
            except Exception as e:
                print("Failed to load demon icon:", e)
            else:
                button.setIcon(icon.icon)
                button.setIconSize(icon.size_div(2))
        button.setText(f"Demon {demon_number}: {demon_txt}")

    def stack_refresh(self):
        for demon_number, button in enumerate(self.demons):
            self.demon_button_refresh(demon_number, button)

    def demon_editor(self, demon_number: int):
        demon = self.save.demon(demon_number)
        return lambda: self.stack_add(
            DemonEditorScreen(demon, self)
        )


class ItemEditorWidget(QScrollArea, GameScreenMixin, AppliableWidget):
    def __init__(self, items: List[Item], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: List[Tuple[ItemEditor, QLabel, QU8]] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QGridLayout()
        self.inner.setLayout(self.l)

        for i, item_meta in enumerate(items):
            item = self.save.items.from_meta(item_meta)
            label = QLabel(item.name, self.inner)
            desc = item.item_meta.desc
            if desc is not None:
                label.setToolTip(desc)
            self.l.addWidget(label, i, 1)
            try:
                pak = ICON_LOADER.element_icon(item.item_meta.icon)
            except Exception as e:
                print("Failed to load element icon:", e)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel(self.inner)
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                if desc is not None:
                    icon.setToolTip(desc)
                self.l.addWidget(icon, i, 0)
            limit_label = QLabel(
                "Limit: " + str(item.limit), self.inner
            )
            if desc is not None:
                limit_label.setToolTip(desc)
            self.l.addWidget(limit_label, i, 2)
            amount_box = QU8(self.inner)
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
            widget = ItemEditorWidget(items, self)
            self.tabs.append(widget)
            self.addTab(widget, name)

    def stack_refresh(self):
        for tab in self.tabs:
            tab.stack_refresh()

    def on_apply_changes(self):
        for tab in self.tabs:
            tab.on_apply_changes()


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
        self.obj = self.save.alignment
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
            byte_editor = self.obj.at_offset(byte.offset)
            for bit in byte.bits:
                box = self.checkboxmap[byte.offset * 8 + bit.bit]
                box.setChecked(byte_editor.get_flag(bit.bit))

    def on_apply_changes(self):
        for byte in ALIGNMENT_DATA:
            byte_editor = self.obj.at_offset(byte.offset)
            for bit in byte.bits:
                box = self.checkboxmap[byte.offset * 8 + bit.bit]
                byte_editor.set_flag(bit.bit, box.isChecked())


class SettingsEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout(self)
        self.difficulty = MComboBox(self)
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

        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.macca = QU32(self)
        self.macca_label = QLabel(self)
        self.macca_label.setText("Macca:")
        self.l.addLayout(hboxed(self.macca_label, self.macca))
        self.menu_buttons = []

        for name, cls in [
            ("DLC", DlcEditorScreen),
            ("Player", PlayerEditorScreen),
            ("Demons", DemonSelectorScreen),
            ("Items", ItemEditorScreen),
            ("Alignment", AlignmentEditorScreen),
            ("Settings", SettingsEditorScreen),
        ]:
            widget = QPushButton(name, self)
            widget.clicked.connect(self.spawner(cls))
            self.l.addWidget(widget)
            self.menu_buttons.append(widget)

        self.l.addStretch()

    def stack_refresh(self):
        self.macca.setValue(self.save.macca)

    def on_apply_changes(self):
        self.macca.setattr_if_modified(self.save, "macca")
