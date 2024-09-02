from PySide6.QtWidgets import QPushButton

from .demonlike import DemonLikeEditorScreen
from .names import NameEditorScreen
from .shared import GameScreenMixin


class PlayerEditorScreen(DemonLikeEditorScreen):
    def __init__(self, *args, **kwargs):
        GameScreenMixin.mixin(self)
        super().__init__(self.save.player, *args, **kwargs)
        self.setLayout(self.dl_layout)

        for i, name, fun in [
            (0, "Names", lambda: NameEditorScreen(
                self.save.player.names
            )),
        ]:
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.dl_layout.insertWidget(i, button)
