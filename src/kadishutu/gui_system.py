from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .gui_common import SaveScreenMixin


class SystemSaveEditorScreen(SaveScreenMixin, QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout(self)
        self.setLayout(self.l)
        label = QLabel("Not implemented", self)
        self.l.addWidget(label)
        label = QLabel("Click File -> Close to close this menu", self)
        self.l.addWidget(label)
