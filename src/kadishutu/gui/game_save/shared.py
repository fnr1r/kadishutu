from ..shared import ScreenMixin


class GameScreenMixin(ScreenMixin):
    def mixin(self):
        super().mixin()
        if not self.editor_widget_on_stack:
            return
        assert not hasattr(self, "save")
        self.save = self.game_save_editor.save

    @property
    def game_save_editor(self):
        widget = self.some_save_editor_widget
        from .game_save import GameSaveEditorScreen
        assert isinstance(widget, GameSaveEditorScreen)
        return widget
