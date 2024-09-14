from kadishutu.core.game_save.demonlike import DemonLikeEditor
from typing import List
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from ..shared import QU8, AppliableWidget, hboxed
from .affinities import AffinityEditorScreen
from .potentials import PotentialEditorScreen
from .shared import GameScreenMixin
from .skills import SkillEditorScreen
from .stats import StatEditorScreen


LEVEL_MUT_WARNING = """WARNING: Changing the level from here is ill-advised.
This editor DOES NOT emulate the changes that would occur within the game \
(such as updating base and current stats, learning skills, etc.).
Please, use Gospels or Grimores to level up instead."""
WARN_EMOJI = "⚠️"


class DemonLikeEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    demon: DemonLikeEditor

    def __init__(self, demon: DemonLikeEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.demon = demon
        self.dl_layout = QVBoxLayout()

        self.side_panel_widgets: List[QWidget] = []

        level_label = QLabel(f"Level ({WARN_EMOJI})")
        level_label.setToolTip(LEVEL_MUT_WARNING)
        self.level_box = QU8()
        self.level_box.setToolTip(LEVEL_MUT_WARNING)
        self.dl_layout.addLayout(hboxed(
            level_label,
            self.level_box
        ))

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

    def stack_refresh(self):
        self.level_box.setValue(self.demon.level)

    def on_apply_changes(self):
        self.level_box.setattr_if_modified(self.demon, "level")
