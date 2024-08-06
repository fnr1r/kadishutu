from enum import Enum, auto
from pathlib import Path
import sys
from typing import List, Optional
from PySide6 import QtWidgets
from PySide6.QtGui import QCloseEvent
#from PySide6.QtWidgets import (
#    QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
#    QMainWindow, QPushButton, QVBoxLayout, QWidget
#)
from PySide6.QtWidgets import *

from .file_handling import DecryptedSave
from .game import SaveEditor


class GameSaveEditor(QWidget):
    path: Path
    save: SaveEditor

    def __init__(self, path: Path, save: SaveEditor, close_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.save = save
        self.close_callback = close_callback

    def closeEvent(self, event: QCloseEvent) -> None:
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
        editor = GameSaveEditor(self.file_path.path, save, self.editors_cleanup)
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
