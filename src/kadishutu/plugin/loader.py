
from kadishutu.paths import APPDIRS
from kadishutu.tools.eprint import eprintf
from kadishutu.tools.singleton import AbstractSingleton
from pathlib import Path
from typing import List

from .meta import Plugin


PLUGINS_PATH = APPDIRS.data_path / "plugins"


class PluginManager(AbstractSingleton):
    plugins: List[Plugin] = []

    def reload(self):
        if not PLUGINS_PATH.exists():
            return
        def loadp(path: Path):
            plugin = Plugin.try_load(path)
            if plugin is None:
                eprintf("Failed to load plugin {}", path.name)
            return plugin
        self.plugins = [
            plugin
            for plugin in [
                loadp(plug_path)
                for plug_path in PLUGINS_PATH.iterdir()
            ]
            if plugin is not None
        ]

    def which_have_stage(self, stage: str) -> List[Plugin]:
        return [
            plugin
            for plugin in self.plugins
            if plugin.manifest.stage == stage
        ]

    def exec(self, stage: str):
        for plugin in self.which_have_stage(stage):
            plugin.exec()


PLUGIN_MANAGER = PluginManager()
