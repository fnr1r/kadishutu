from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from .demonlike import DemonLikeEditorScreen
from .affinities import AffinityEditorScreen
from .names import NameEditorScreen
from .potentials import PotentialEditorScreen
from .shared import GameScreenMixin
from .skills import SkillEditorScreen
from .stats import StatEditorScreen


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
