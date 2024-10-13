from kadishutu.plugin.loader import PLUGIN_MANAGER
from PySide6.QtWidgets import QTabWidget

from .shared import GameScreenMixin


class GameSavePluginScreen(QTabWidget, GameScreenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PLUGIN_MANAGER.exec("gui_game_component")
