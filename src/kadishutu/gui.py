from abc import abstractmethod
from enum import Enum, auto
from pathlib import Path
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple
from PySide6.QtGui import QCloseEvent
#from PySide6.QtWidgets import (
#    QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
#    QMainWindow, QPushButton, QVBoxLayout, QWidget
#)
from PySide6.QtWidgets import *

from .data.demons import DEMON_ID_MAP, DEMON_NAME_MAP
from .data.element_icons import Element
from .data.items import CONSUMABLES_RANGE, items_from
from .data.skills import SKILL_ID_MAP, SKILL_NAME_MAP
from .demons import STATS_NAMES, DemonEditor, HealableEditor, StatsEditor
from .file_handling import DecryptedSave
from .game import SaveEditor
from .gui_icons import ICON_LOADER
from .items import ItemEditor
from .skills import Skill, SkillEditor


U16_MAX = 2 ** 16 -1
# RuntimeWarning: libshiboken: Overflow: Value 7378697629483820646 exceeds
# limits of type  [signed] "i" (4bytes).
SHIBOKEN_MAX = 2 ** 31 - 1


MAIN_WINDOW: "MainWindow"


class QModifiedMixin:
    _modified: bool = False

    def getModified(self) -> bool:
        return self._modified

    def setModified(self, modified: bool):
        self._modified = modified

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError

    def update_if_modified(self, updater: Callable[..., None]):
        if self.getModified():
            updater(self.get_value())
            self.setModified(False)

    def setattr_if_modified(self, obj: object, attr: str):
        if self.getModified():
            obj.__setattr__(attr, self.get_value())
            self.setModified(False)


class OnStackRemovedHook:
    @abstractmethod
    def on_stack_removed(self):
        raise NotImplementedError


class QU8(QSpinBox, QModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(2 ** 8 -1)
        self.valueChanged.connect(lambda _: self.setModified(True))

    def get_value(self) -> int:
        return self.value()


class QU16(QSpinBox, QModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(U16_MAX)
        self.valueChanged.connect(lambda _: self.setModified(True))

    def get_value(self) -> int:
        return self.value()


class QU32(QSpinBox, QModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(SHIBOKEN_MAX)
        self.valueChanged.connect(lambda _: self.setModified(True))

    def get_value(self) -> int:
        return self.value()


class EditorMixin:
    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mixin()

    def mixin(self):
        parent = self.game_save_editor
        self.save = parent.save
        self.stack_add = MAIN_WINDOW.stack_add
        self.stack_remove = MAIN_WINDOW.stack_remove

    def stack_refresh(self): ...

    @property
    def game_save_editor(self) -> "GameSaveEditor":
        widget = MAIN_WINDOW.inner.widget_stack[1]
        assert isinstance(widget, GameSaveEditor)
        return widget

    def dispatch(self, cls):
        widget = cls(self)
        self.stack_add(widget)

    def spawner(self, fun):
        return lambda: self.stack_add(fun())


class GWidget(EditorMixin, QWidget):
    pass


class GTabWidget(EditorMixin, QTabWidget):
    pass


class GScrollArea(EditorMixin, QScrollArea):
    pass


class AppliableWidget:
    @abstractmethod
    def apply_changes(self):
        raise NotImplementedError


def hboxed(parent: QWidget, *args: QWidget):
    w = QWidget(parent)
    l = QHBoxLayout()
    l.setContentsMargins(0, 0, 0, 0)
    w.setLayout(l)
    for widget in args:
        widget.setParent(w)
        l.addWidget(widget)
    return w


class StatEditorScreen(GWidget, AppliableWidget):
    STAT_TYPES = ["Base", "Changes", "Current", "Healable"]

    def __init__(self, stats: StatsEditor, healable: HealableEditor, *args, **kwargs):
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

    def apply_changes(self):
        for ty, v in self.widgets.items():
            for stat, widget in v.items():
                widget.update_if_modified(self.apply_widget(ty, stat))


class AbstractStrIntMap(QWidget, QModifiedMixin):
    def __init__(self, items: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        QModifiedMixin.__init__(self)
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
        self.setModified(True)
        self.str_box.setCurrentText(self.int_to_str(value))

    def str_changed(self, value: str):
        self.setModified(True)
        self.int_box.setValue(self.str_to_int(value))


class SkillBox(AbstractStrIntMap, QModifiedMixin):
    def __init__(self, skill: Skill, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QModifiedMixin.__init__(self)
        self.skill = skill
        self.int_box.setMaximum(U16_MAX)

    def refresh(self):
        self.int_box.setValue(self.skill.id)
        self.str_box.setCurrentText(self.skill.name)

    def apply_changes(self):
        if self.getModified:
            self.skill.id = self.int_box.value()
            self.setModified(False)

    def int_to_str(self, value: int) -> str:
        return SKILL_ID_MAP[value].name

    def str_to_int(self, value: str) -> int:
        return SKILL_NAME_MAP[value].id


class SkillEditorScreen(GWidget, AppliableWidget):
    def __init__(self, skills: SkillEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.widgets: List[Tuple[QWidget, QLabel, SkillBox, QU16]] = []

        for i in range(8):
            skill = skills.slot(i)
            label = QLabel(f"Skill {i + 1}", self)
            skill_box = SkillBox(skill, list(SKILL_NAME_MAP.keys()), self)
            mystery_box = QU16(self)
            widget = hboxed(self, label, skill_box, mystery_box)
            self.l.addWidget(widget)
            self.widgets.append((widget, label, skill_box, mystery_box))

        self.l.addStretch()

    def stack_refresh(self):
        for i in range(8):
            (_, _, skill_box, mystery_box) = self.widgets[i]
            skill_box.refresh()
            skill = skill_box.skill
            mystery_box.setValue(skill._unknown)

    def apply_changes(self):
        for i in range(8):
            (_, _, skill_box, mystery_box) = self.widgets[i]
            skill_box.apply_changes()
            mystery_box.setattr_if_modified(skill_box.skill, "_unknown")


class PlayerEditorScreen(GWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        for name, fun in [
            ("Stats", lambda: StatEditorScreen(
                self.save.player.stats, self.save.player.healable, self
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.save.player.skills, self
            ))
        ]:
            button = QPushButton(name, self)
            button.clicked.connect(self.spawner(fun))
            self.l.addWidget(button)
            self.buttons.append(button)

        self.l.addStretch()


class DemonIdnWidget(QWidget, QModifiedMixin):
    def __init__(self, demon: DemonEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QModifiedMixin.__init__(self)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.id_label = QLabel("ID:", self)
        self.id_box = QSpinBox(self)
        self.id_box.setMaximum(U16_MAX)
        self.id_box.setValue(demon.demon_id)
        self.id_box.valueChanged.connect(self.id_changed)
        self.id_widget = hboxed(self, self.id_label, self.id_box)
        self.layout().addWidget(self.id_widget)

        self.name_label = QLabel("Name:", self)
        self.name_box = QComboBox(self)
        self.name_box.addItems(list(DEMON_NAME_MAP.keys()))
        self.name_box.setCurrentText(demon.name)
        self.name_box.currentTextChanged.connect(self.name_changed)
        self.name_widget = hboxed(self, self.name_label, self.name_box)
        self.layout().addWidget(self.name_widget)

    def get_value(self) -> int:
        return self.id_box.value()

    def id_changed(self, id: int):
        self.setModified(True)
        try:
            self.name_box.setCurrentText(DEMON_ID_MAP[id]["name"])
        except KeyError:
            pass

    def name_changed(self, name: str):
        self.setModified(True)
        self.id_box.setValue(DEMON_NAME_MAP[name]["id"])


class DemonEditorScreen(GWidget, AppliableWidget):
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

    def apply_changes(self):
        self.demon_idn_widget.setattr_if_modified(self.demon, "demon_id")


class DemonSelectorScreen(GWidget):
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
            except:
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


class ItemEditorWidget(GScrollArea, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: List[Tuple[ItemEditor, QLabel, QU8]] = []

        self.setWidgetResizable(True)
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.l = QGridLayout()
        self.inner.setLayout(self.l)

        for i, item_meta in enumerate(items_from(CONSUMABLES_RANGE)):
            item = self.save.items.from_meta(item_meta)
            label = QLabel(item.name, self.inner)
            try:
                pak = ICON_LOADER.element_icon(Element.Misc)
            except Exception as e:
                print("Failed to load element icon:", e)
            else:
                pix = pak.pixmap.scaled(pak.size_div(2))
                icon = QLabel(self.inner)
                icon.setFixedSize(pix.size())
                icon.setPixmap(pix)
                self.l.addWidget(icon, i, 0)
            self.l.addWidget(label, i, 1)
            amount_box = QU8(self.inner)
            self.l.addWidget(amount_box, i, 2)
            self.items.append((item, label, amount_box))

    def stack_refresh(self):
        for item, _, amount_box in self.items:
            amount_box.setValue(item.amount)

    def apply_changes(self):
        for item, _, amount_box in self.items:
            amount_box.setattr_if_modified(item, "amount")


class ItemEditorScreen(GTabWidget, AppliableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs: List[ItemEditorWidget] = []
        
        for name, func in [
            ("Consumables", lambda: ItemEditorWidget(self)),
            ("Relics", lambda: GWidget(self)),
            ("Key Items", lambda: GWidget(self))
        ]:
            widget = func()
            self.tabs.append(widget)
            self.addTab(widget, name)

    def stack_refresh(self):
        for tab in self.tabs:
            tab.stack_refresh()

    def apply_changes(self):
        for tab in self.tabs:
            tab.apply_changes()


class GameSaveEditor(QWidget, AppliableWidget):
    path: Path
    raw_save: DecryptedSave
    save: SaveEditor
    modified: bool

    def __init__(
        self,
        path: Path,
        raw_save: DecryptedSave,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.path = path
        self.raw_save = raw_save
        self.save = SaveEditor(raw_save)
        self.modified = False

        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.macca = QU32(self)
        self.macca.setValue(self.save.macca)
        self.macca_label = QLabel(self)
        self.macca_label.setText("Macca:")
        w = hboxed(self, self.macca_label, self.macca)
        self.l.addWidget(w)
        self.menu_buttons = []

        for name, cls in [
            ("Player", PlayerEditorScreen),
            ("Demons", DemonSelectorScreen),
            ("Items", ItemEditorScreen)
        ]:
            widget = QPushButton(name, self)
            widget.clicked.connect(self.spawner(cls))
            self.l.addWidget(widget)
            self.menu_buttons.append(widget)

        self.l.addStretch()

    def spawner(self, cls, *args, **kwargs):
        return lambda: MAIN_WINDOW.stack_add(cls(self, *args, **kwargs))

    def apply_changes(self):
        self.macca.setattr_if_modified(self.save, "macca")


class SaveType(Enum):
    SysSave = auto()
    GameSave = auto()


class FileSelector(QWidget):
    _path: Path

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.file_path_display = QLineEdit(self)
        self.file_path_display.setReadOnly(True)
        self.layout().addWidget(self.file_path_display)
        self.file_open_button = QPushButton("Select", self)
        self.file_open_button.clicked.connect(self.on_select_clicked)
        self.layout().addWidget(self.file_open_button)
    
    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: Path):
        self._path = path
        self.file_path_display.setText(str(path))

    def on_select_clicked(self):
        (pathstr, _) = QFileDialog.getOpenFileName(self)
        if not pathstr:
            return
        path = Path(pathstr)
        self._path = path
        self.file_path_display.setText(pathstr)


class FileSelectorPreview(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.name = QLabel(self)
        self.layout().addWidget(self.name)
        self.location = QLabel(self)
        self.location.setText("Location: TODO")
        self.layout().addWidget(self.location)
        self.difficulty = QLabel(self)
        self.layout().addWidget(self.difficulty)
        self.play_time = QLabel(self)
        self.layout().addWidget(self.play_time)
        self.date = QLabel(self)
        self.layout().addWidget(self.date)
        self.empty()

    def empty(self):
        self.name.setText("Name: N/A")
        self.difficulty.setText("Difficulty: N/A")
        self.play_time.setText("Play Time: N/A")
        self.date.setText("Date: N/A")

    def update(self, save: SaveEditor):
        self.name.setText("Name: " + save.player.names.save_name.get())
        self.difficulty.setText("Difficulty: " + save.difficulty.name)
        self.play_time.setText("Play Time: " + str(save.play_time))
        self.date.setText("Date: " + str(save.time_of_saving))


class FileSelectorMenu(QWidget):
    raw: Optional[DecryptedSave] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.file_path = FileSelector(self)
        self.file_path.file_path_display.textChanged.connect(self.file_selected)
        self.layout().addWidget(self.file_path)
        self.file_type = QComboBox(self)
        self.file_type.addItems([ty.name for ty in SaveType])
        self.file_type.setCurrentText(SaveType.GameSave.name)
        self.layout().addWidget(self.file_type)
        self.file_preview = FileSelectorPreview(self)
        self.layout().addWidget(self.file_preview)
        self.file_open = QPushButton("Open", self)
        self.file_open.setEnabled(False)
        self.file_open.clicked.connect(self.on_file_open)
        self.layout().addWidget(self.file_open)

    def on_file_open(self):
        assert self.raw
        if self.ty == SaveType.SysSave:
            QMessageBox.critical(
                self, "Error", "Editing SysSave files is not implemented.",
                QMessageBox.StandardButton.Ok
            )
            return
        editor = GameSaveEditor(self.file_path.path, self.raw, self)
        MAIN_WINDOW.stack_add(editor)

    def file_selected(self):
        path = self.file_path.path
        self.raw = DecryptedSave.auto_open(path)
        self.file_open.setEnabled(True)
        raw = self.raw
        if len(raw.data) == 0x12e0:
            self.ty = SaveType.SysSave
            self.file_preview.empty()
        elif len(raw.data) == 0x6dc90:
            self.ty = SaveType.GameSave
            self.file_type.setCurrentText(self.ty.name)
            save = SaveEditor(raw)
            self.file_preview.update(save)
        else:
            self.raw = None
            self.file_preview.empty()


class LocationBar(QScrollArea):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedHeight(10)
        self.inner = QWidget(self)
        self.setWidget(self.inner)
        self.inner.setLayout(QHBoxLayout())
        self.inner.layout().setContentsMargins(0, 0, 0, 0)
        #self.scroll_bar = QScrollBar(QtCore.Orientation.Horizontal, self.scrolla)
        #self.scrolla.setHorizontalScrollBar(self.scroll_bar)
        #self.scrolla.horizontalScrollBar().setEnabled(True)
        #self.scrolla.setHorizontalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.inner.setHorizontalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll_area.setWidgetResizable(True)
        #self.inner.setMaximumSize(9999, self.inner.maximumSize().height())
        #self.inner = QWidget(self.scrolla)
        #self.setMaximumHeight(40)
        for i in range(10):
            txt = chr(64 + i + 1) * 6
            b = QPushButton(txt, self.inner)
            b.setContentsMargins(0, 0, 0, 0)
            self.inner.layout().addWidget(b)
        #self.a = QLabel("aaaaa", self)
        #self.addWidget(self.a)


class ManagedStackWidget(QWidget):
    widget_stack: List[QWidget]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_stack = []
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # TODO
        #self.location_bar = LocationBar(self)
        #self.layout().addWidget(self.location_bar)
        self.stack = QStackedWidget(self)
        self.layout().addWidget(self.stack)

    @property
    def should_show_navigation(self) -> bool:
        return len(self.widget_stack) > 1

    def stack_add(self, widget: QWidget):
        if isinstance(widget, EditorMixin):
            widget.stack_refresh()
        widget.setParent(self)
        self.widget_stack.append(widget)
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)
        #if self.should_show_navigation:
        #    self.location_bar.show()

    def stack_remove(self):
        if len(self.widget_stack) < 2:
            raise ValueError("Refusing to go back with widget stack at 1")
        widget = self.widget_stack.pop()
        if isinstance(widget, OnStackRemovedHook):
            widget.on_stack_removed()
        self.stack.removeWidget(widget)
        self.stack.setCurrentWidget(self.widget_stack[-1])
        #if len(self.widget_stack) < 2:
        #    self.location_bar.hide()

    @property
    def top_widget(self) -> QWidget:
        return self.widget_stack[-1]

    @property
    def editor_widget(self) -> GameSaveEditor:
        widget = self.widget_stack[1]
        assert isinstance(widget, GameSaveEditor)
        return widget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #self.resize(1280, 720)

        self.file_menu = QMenu("File", self)
        self.save_button = self.file_menu.addAction("Save")
        self.save_button.triggered.connect(self.on_save)
        self.save_as_button = self.file_menu.addAction("Save as")
        self.save_as_button.triggered.connect(self.on_save_as)
        self.close_button = self.file_menu.addAction("Close")
        self.close_button.triggered.connect(self.on_file_close)
        self.file_menu.addSeparator()
        self.quit_button = self.file_menu.addAction("Quit")
        self.quit_button.triggered.connect(self.close)
        self.menuBar().addMenu(self.file_menu)
        self.edit_menu = QMenu("Edit", self)
        self.undo_button = self.edit_menu.addAction("Undo")
        #self.undo_button.triggered.connect(self.on_save)
        self.menuBar().addMenu(self.edit_menu)
        self.menu_separator = self.menuBar().addSeparator()
        self.apply_button = self.menuBar().addAction("Apply")
        self.apply_button.triggered.connect(self.on_apply)
        self.back_button = self.menuBar().addAction("Back")
        self.back_button.triggered.connect(self.on_back)

        self.inner = ManagedStackWidget(self)
        self.setCentralWidget(self.inner)

        self.file_selector = FileSelectorMenu(self)
        self.stack_add(self.file_selector)
        self.back_button.setEnabled(False)

    def stack_add(self, widget: QWidget):
        self.inner.stack_add(widget)
        self.refresh_nav_actions()

    def stack_remove(self):
        self.inner.stack_remove()
        self.refresh_nav_actions()

    def refresh_nav_actions(self):
        if len(self.inner.widget_stack) > 2:
            self.back_button.setEnabled(True)
        else:
            self.back_button.setEnabled(False)
        top_widget = self.inner.top_widget
        if isinstance(top_widget, AppliableWidget):
            self.apply_button.setEnabled(True)
        else:
            self.apply_button.setEnabled(False)
        if len(self.inner.widget_stack) > 1:
            self.save_button.setEnabled(True)
            self.save_as_button.setEnabled(True)
            self.close_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
            self.save_as_button.setEnabled(False)
            self.close_button.setEnabled(False)
        #self.statusBar().showMessage(" > ".join([
        #    i.__class__.__name__
        #    for i in self.inner.widget_stack
        #]))

    def on_back(self):
        self.stack_remove()

    def on_apply(self):
        widget = self.inner.top_widget
        if not isinstance(widget, AppliableWidget):
            raise NotImplementedError
        self.inner.editor_widget.modified = True
        widget.apply_changes()
        for widget in self.inner.widget_stack:
            if not isinstance(widget, EditorMixin):
                continue
            widget.stack_refresh()

    def on_save(self):
        if not self.inner.should_show_navigation:
            return
        widget = self.inner.editor_widget
        widget.raw_save.encrypt().save(widget.path)
        self.inner.editor_widget.modified = False

    def on_save_as(self):
        (pathstr, _) = QFileDialog.getSaveFileName(self)
        if not pathstr:
            return
        path = Path(pathstr)
        self.inner.editor_widget.raw_save.encrypt().save(path)
        self.inner.editor_widget.modified = False

    def on_file_close(self):
        if self.alert_abandoning_modifications():
            return
        while len(self.inner.widget_stack) > 1:
            self.stack_remove()

    def alert_abandoning_modifications(self) -> bool:
        if not (self.inner.should_show_navigation and
            self.inner.editor_widget.modified):
            return False
        prompt = QMessageBox.question(
            self, "", "Discard changes?",
            QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No
        )
        if prompt == QMessageBox.StandardButton.No.value:
            return True
        return False

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.alert_abandoning_modifications():
            event.ignore()
            return
        return super().closeEvent(event)


def gui_main(args):
    app = QApplication()
    global MAIN_WINDOW
    MAIN_WINDOW = MainWindow()
    if args.file:
        MAIN_WINDOW.file_selector.file_path.path = args.file
        MAIN_WINDOW.file_selector.file_open.click()
    MAIN_WINDOW.show()
    sys.exit(app.exec())
