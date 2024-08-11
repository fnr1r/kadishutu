from pathlib import Path
import sys
from typing import List, Optional
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMessageBox, QPushButton, QScrollArea, QStackedWidget,
    QVBoxLayout, QWidget
)
# NOTE: I wish Python had a better tool for this
# Like (for example) rustfmt

from .file_handling import DecryptedSave
from .game import SaveEditor
from .gui_common import AppliableWidget, OnStackRemovedHook, SaveType
from .gui_game import EditorMixin, GameSaveEditorScreen


MAIN_WINDOW: "MainWindow"


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
        file_path_display = self.file_path.file_path_display
        file_path_display.textChanged.connect(self.file_selected)
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
        editor = GameSaveEditorScreen(self.file_path.path, self.raw, self)
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
    def editor_widget(self) -> GameSaveEditorScreen:
        widget = self.widget_stack[1]
        assert isinstance(widget, GameSaveEditorScreen)
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
        self.undo_button.triggered.connect(self.on_undo)
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
            self.undo_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
            self.save_as_button.setEnabled(False)
            self.close_button.setEnabled(False)
            self.undo_button.setEnabled(False)
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
        widget.on_apply_changes()
        for widget in self.inner.widget_stack:
            if not isinstance(widget, EditorMixin):
                continue
            widget.stack_refresh()

    def on_save(self):
        if not self.inner.should_show_navigation:
            return
        widget = self.inner.editor_widget
        widget.raw_save.encrypt().save(widget.path)
        widget.modified = False

    def on_save_as(self):
        (pathstr, _) = QFileDialog.getSaveFileName(self)
        if not pathstr:
            return
        path = Path(pathstr)
        widget = self.inner.editor_widget
        widget.raw_save.encrypt().save(path)
        widget.modified = False

    def on_file_close(self):
        if self.alert_abandoning_modifications():
            return
        while len(self.inner.widget_stack) > 1:
            self.stack_remove()

    def on_undo(self):
        widget = self.inner.top_widget
        if not isinstance(widget, EditorMixin):
            raise NotImplementedError
        widget.stack_refresh()

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
    widget = MainWindow()
    global MAIN_WINDOW
    MAIN_WINDOW = widget
    if args.file:
        widget.file_selector.file_path.path = args.file
        widget.file_selector.file_open.click()
    widget.show()
    sys.exit(app.exec())
