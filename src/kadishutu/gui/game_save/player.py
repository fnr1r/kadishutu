from PySide6.QtWidgets import QLabel, QPushButton

from kadishutu.core.game_save.player import PlayerEditor

from ..shared import QU16, AppliableWidget, hboxed
from .demonlike import DemonLikeEditorScreen
from .names import NameEditorScreen
from .shared import GameScreenMixin


class PlayerEditorScreen(DemonLikeEditorScreen, AppliableWidget):
    def __init__(self, *args, **kwargs):
        GameScreenMixin.mixin(self)
        super().__init__(self.save.player, *args, **kwargs)
        self.setLayout(self.dl_layout)

        for i, (name, fun) in enumerate([
            ("Names", lambda: NameEditorScreen(
                self.save.player.names
            )),
        ], start=self.last_box):
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.dl_layout.insertWidget(i, button)

        self.stat_points_box = QU16()
        self.dl_layout.insertLayout(self.last_box, hboxed(
            QLabel("Stat points"),
            self.stat_points_box,
        ))
        self.last_box += 1

    @property
    def player(self) -> PlayerEditor:
        player = self.demon
        assert isinstance(player, PlayerEditor)
        return player

    def stack_refresh(self):
        super().stack_refresh()
        self.stat_points_box.setValue(self.player.stat_points)

    def on_apply_changes(self):
        super().on_apply_changes()
        self.stat_points_box.setattr_if_modified(self.player, "stat_points")
