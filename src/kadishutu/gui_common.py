from abc import abstractmethod
from enum import Enum, auto
from pathlib import Path
from PySide6.QtWidgets import QWidget

from .file_handling import DecryptedSave


class OnStackRemovedHook:
    @abstractmethod
    def on_stack_removed(self):
        raise NotImplementedError


class AppliableWidget:
    @abstractmethod
    def on_apply_changes(self):
        raise NotImplementedError


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
