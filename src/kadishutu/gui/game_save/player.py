from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from .affinities import AffinityEditorScreen
from .names import NameEditorScreen
from .potentials import PotentialEditorScreen
from .shared import GameScreenMixin
from .skills import SkillEditorScreen
from .stats import StatEditorScreen


class PlayerEditorScreen(QWidget, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        for name, fun in [
            ("Names", lambda: NameEditorScreen(
                self.save.player.names
            )),
            ("Stats", lambda: StatEditorScreen(
                self.save.player.stats, self.save.player.healable
            )),
            ("Skills", lambda: SkillEditorScreen(
                self.save.player.skills, self.save.player.innate_skill
            )),
            ("Affinities", lambda: AffinityEditorScreen(
                self.save.player.affinities
            )),
            ("Potentials", lambda: PotentialEditorScreen(
                self.save.player.potentials
            ))
        ]:
            button = QPushButton(name)
            button.clicked.connect(self.spawner(fun))
            self.l.addWidget(button)

        self.l.addStretch()
