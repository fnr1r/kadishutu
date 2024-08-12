from abc import abstractmethod
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QSpinBox, QWidget

from .file_handling import DecryptedSave


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


class ScreenMixin:
    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mixin()

    def mixin(self):
        from .gui import MAIN_WINDOW
        self.stack_add = MAIN_WINDOW.stack_add
        self.stack_remove = MAIN_WINDOW.stack_remove

    def stack_refresh(self): ...

    def dispatch(self, cls, *args, **kwargs):
        widget = cls(*args, self, **kwargs)
        self.stack_add(widget)

    def spawner(self, fun):
        return lambda: self.stack_add(fun())

    @property
    def editor_widget_on_stack(self) -> bool:
        from .gui import MAIN_WINDOW
        return len(MAIN_WINDOW.inner.widget_stack) > 1

    @property
    def some_save_editor_widget(self) -> QWidget:
        from .gui import MAIN_WINDOW
        widget = MAIN_WINDOW.inner.widget_stack[1]
        return widget


class SaveScreenMixin(ScreenMixin):
    path: Path
    raw_save: DecryptedSave
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
        self.modified = False
