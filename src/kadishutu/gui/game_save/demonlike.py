from kadishutu.core.game_save.demonlike import DemonLikeEditor
from typing import List
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from ..shared import AppliableWidget
from .affinities import AffinityEditorScreen
from .potentials import PotentialEditorScreen
from .shared import GameScreenMixin
from .skills import SkillEditorScreen
from .stats import StatEditorScreen


class DemonLikeEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    demon: DemonLikeEditor

    def __init__(self, demon: DemonLikeEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demon = demon
        self.dl_layout = QVBoxLayout()

        self.side_panel_widgets: List[QWidget] = []

        for name, fun in [
            ("Stats", lambda: StatEditorScreen(
                self.demon.stats, self.demon.healable
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.demon.skills, self.demon.innate_skill
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.demon.affinities
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.demon.potentials
            ))
        ]:
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.side_panel_widgets.append(button)

        for button in self.side_panel_widgets:
            self.dl_layout.addWidget(button)
        self.dl_layout.addStretch()
