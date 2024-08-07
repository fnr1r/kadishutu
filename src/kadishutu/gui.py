from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path
import sys
from typing import Callable, List, Optional
from PySide6 import QtWidgets
import PySide6
import PySide6.QtCore
from PySide6.QtGui import QCloseEvent
#from PySide6.QtWidgets import (
#    QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
#    QMainWindow, QPushButton, QVBoxLayout, QWidget
#)
from PySide6.QtWidgets import *

from .file_handling import DecryptedSave
from .game import SaveEditor


class QModifiedMixin:
    _modified: bool

    def getModified(self) -> bool:
        return self._modified

    def setModified(self, modified: bool):
        self._modified = modified


class QU32(QSpinBox, QModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(2 ** 31 -1)
        self.valueChanged.connect(lambda _: self.setModified(True))


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
        self.stack_add = parent.inner_add
        self.stack_remove = parent.inner_back

    @property
    def game_save_editor(self) -> "GameSaveEditor":
        widget = self.parentWidget()
        for _ in range(4):
            if isinstance(widget, GameSaveEditor):
                return widget
            widget = widget.parentWidget()
        raise Exception

    @property
    def stack_widget(self) -> QStackedWidget:
        return self.game_save_editor.inner

    def dispatch(self, cls):
        widget = cls(self)
        self.stack_add(widget)


class GWidget(EditorMixin, QWidget):
    pass


class GScrollArea(EditorMixin, QScrollArea):
    pass


class SavableWidget:
    @abstractmethod
    def save_changes(self):
        ...


def hboxed(parent: QWidget, *args: QWidget):
    w = QWidget(parent)
    l = QHBoxLayout()
    l.setContentsMargins(0, 0, 0, 0)
    w.setLayout(l)
    for widget in args:
        widget.setParent(w)
        l.addWidget(widget)
    return w


class DemonSelectorScreen(GWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QGridLayout()
        self.setLayout(self.l)
        #self.outer = QScrollArea(self)
        #self.outer.setWidget(self)
        self.demons = []
        for demon_number in range(24):
            demon = self.save.demon(demon_number)
            if demon.demon_id == 0xffff:
                demon_txt = "None"
            else:
                try:
                    demon_txt = demon.name
                except:
                    demon_txt = f"Unknown ({demon.demon_id})"
            sel = QPushButton(f"Demon {demon_number}: {demon_txt}", self)
            row = int(demon_number / 4)
            column = demon_number % 4
            self.l.addWidget(sel, row, column)
            self.demons.append(sel)


class GameMainScreen(GWidget, SavableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.macca = QU32(self)
        self.macca.setValue(self.save.macca)
        self.macca_label = QLabel(self)
        self.macca_label.setText("Macca:")
        w = hboxed(self, self.macca_label, self.macca)
        self.layout().addWidget(w)
        self.demons_menu = QPushButton("Demons", self)
        self.demons_menu.clicked.connect(self.open_demons_menu)
        self.layout().addWidget(self.demons_menu)

    def open_demons_menu(self):
        widget = DemonSelectorScreen(self)
        self.stack_add(widget)

    def save_changes(self):
        if self.macca.getModified():
            self.save.macca = self.macca.value()
            self.macca.setModified(False)


class GameSaveEditor(QMainWindow):
    path: Path
    save: SaveEditor
    modified: bool
    widget_stack: List[QWidget]

    def __init__(self, path: Path, save: SaveEditor, close_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.save = save
        self.close_callback = close_callback
        self.modified = False
        self.widget_stack = []
        #self.resize(1280, 720)
        self.file_menu = QMenu("File", self)
        self.file_menu.addAction("Save")
        self.file_menu.addAction("Save as")
        self.menuBar().addMenu(self.file_menu)
        self.menu_separator = self.menuBar().addSeparator()
        self.save_button = self.menuBar().addAction("Apply")
        self.save_button.triggered.connect(self.on_save)
        self.back_button = self.menuBar().addAction("Back")
        self.back_button.triggered.connect(self.inner_back)
        self.inner = QStackedWidget(self)
        self.setCentralWidget(self.inner)
        self.inner_add(GameMainScreen(self.inner))
        self.back_button.setEnabled(False)

    def on_save(self):
        widget = self.widget_stack[-1]
        if not isinstance(widget, SavableWidget):
            raise NotImplementedError
        self.modified = True
        widget.save_changes()

    def refresh_save_action(self, widget: QWidget):
        if isinstance(widget, SavableWidget):
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def inner_add(self, widget: QWidget):
        widget.setParent(self.inner)
        self.widget_stack.append(widget)
        self.inner.addWidget(widget)
        self.inner.setCurrentWidget(widget)
        self.back_button.setEnabled(True)
        self.refresh_save_action(widget)

    def inner_back(self):
        if len(self.widget_stack) < 2:
            raise ValueError("Refusing to go back with widget stack at 1")
        widget = self.widget_stack.pop()
        self.inner.removeWidget(widget)
        #self.inner.setCurrentWidget(self.widget_stack[-1])
        if len(self.widget_stack) < 2:
            self.back_button.setEnabled(False)
        self.refresh_save_action(self.widget_stack[-1])

    @property
    def game_main_screen(self) -> GameMainScreen:
        widget = self.widget_stack[0]
        assert isinstance(widget, GameMainScreen)
        return widget

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.modified:
            prompt = QMessageBox.question(
                self, "", "Discard changes?",
                QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No
            )
            if prompt == QMessageBox.StandardButton.No.value:
                event.ignore()
                return
        self.close_callback(self)
        return super().closeEvent(event)


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

    def on_file_selected(self, file: str):
        self.path = Path(file)

    def on_select_clicked(self):
        dialog = QFileDialog(self)
        dialog.fileSelected.connect(self.on_file_selected)
        dialog.exec()


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
        self.difficulty.setText("Difficulty: TODO")
        self.layout().addWidget(self.difficulty)
        self.play_time = QLabel(self)
        self.layout().addWidget(self.play_time)
        self.date = QLabel(self)
        self.layout().addWidget(self.date)
        self.empty()

    def empty(self):
        self.name.setText("Name: N/A")
        self.play_time.setText("Play Time: N/A")
        self.date.setText("Date: N/A")

    def update(self, save: SaveEditor):
        self.name.setText("Name: " + save.player.names.save_name.get())
        self.play_time.setText("Play Time: " + str(save.play_time))
        self.date.setText("Date: " + str(save.time_of_saving))


class FileSelectorMenu(QWidget):
    raw: Optional[DecryptedSave] = None
    editors: List[QWidget]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.editors = []
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
        self.file_edit = QPushButton("Edit", self)
        self.file_edit.setEnabled(False)
        self.file_edit.clicked.connect(self.on_file_edit)
        self.layout().addWidget(self.file_edit)

    def on_file_edit(self):
        assert self.raw
        if self.ty == SaveType.SysSave:
            QMessageBox.critical(
                self, "Error", "Editing SysSave files is not implemented.",
                QMessageBox.StandardButton.Ok
            )
            return
        save = SaveEditor(self.raw)
        editor = GameSaveEditor(self.file_path.path, save, self.editors_cleanup, self)
        editor.show()
        self.editors.append(editor)

    def editors_cleanup(self, value: QWidget):
        self.editors.remove(value)

    def file_selected(self):
        path = self.file_path.path
        self.raw = DecryptedSave.auto_open(path)
        self.file_edit.setEnabled(True)
        raw = self.raw
        if len(raw.data) == 4832:
            self.ty = SaveType.SysSave
        else:
            assert len(raw.data) == 449680
            self.ty = SaveType.GameSave
        self.file_type.setCurrentText(self.ty.name)
        if self.ty == SaveType.SysSave:
            self.file_preview.empty()
            return
        save = SaveEditor(raw)
        self.file_preview.update(save)


class MainWindow(QMainWindow):
    def __init__(self, path: Optional[Path], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file_selector = FileSelectorMenu(self)
        self.setCentralWidget(self.file_selector)
        if not path:
            return
        self.file_selector.file_path.path = path


def gui_main(args):
    app = QApplication()
    MAIN_WINDOW = MainWindow(args.file)
    MAIN_WINDOW.show()
    sys.exit(app.exec())
