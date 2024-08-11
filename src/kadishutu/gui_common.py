from abc import abstractmethod
from enum import Enum, auto
from typing import Any, Callable
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QSpinBox, QWidget


U16_MAX = 2 ** 16 - 1
# RuntimeWarning: libshiboken: Overflow: Value 7378697629483820646 exceeds
# limits of type  [signed] "i" (4bytes).
SHIBOKEN_MAX = 2 ** 31 - 1


class OnStackRemovedHook:
    @abstractmethod
    def on_stack_removed(self):
        raise NotImplementedError


class AppliableWidget:
    @abstractmethod
    def on_apply_changes(self):
        raise NotImplementedError


class ModifiedMixin:
    _modified: bool = False

    def get_modified(self) -> bool:
        return self._modified

    def set_modified(self, modified: bool):
        self._modified = modified

    def flag_as_modified(self):
        self.set_modified(True)

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError

    def update_if_modified(self, updater: Callable[..., None]):
        if self.get_modified():
            updater(self.get_value())
            self.set_modified(False)

    def setattr_if_modified(self, obj: object, attr: str):
        if self.get_modified():
            obj.__setattr__(attr, self.get_value())
            self.set_modified(False)


class QU8(QSpinBox, ModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(2 ** 8 - 1)
        self.valueChanged.connect(self.flag_as_modified)

    def get_value(self) -> int:
        return self.value()


class QU16(QSpinBox, ModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(U16_MAX)
        self.valueChanged.connect(self.flag_as_modified)

    def get_value(self) -> int:
        return self.value()


class QU32(QSpinBox, ModifiedMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(SHIBOKEN_MAX)
        self.valueChanged.connect(self.flag_as_modified)

    def get_value(self) -> int:
        return self.value()


def boxed(layout: QBoxLayout, parent: QWidget, *args: QWidget):
    widget = QWidget(parent)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)
    for child in args:
        child.setParent(widget)
        layout.addWidget(child)
    return widget


def hboxed(parent: QWidget, *args: QWidget):
    return boxed(QHBoxLayout(), parent, *args)


class SaveType(Enum):
    SysSave = auto()
    GameSave = auto()
