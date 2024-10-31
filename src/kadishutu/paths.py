from os import getenv
from pathlib import Path
import sys

from kadishutu.tools.singleton import AbstractSingleton

if sys.platform == "linux":
    from xdg import xdg_data_home


APP_NAME = "kadishutu"
APP_AUTHOR = "fnrir"

PORTABLE_PREFIX = "_appdata"


class AppDirs(AbstractSingleton):
    #cache_path: Path
    #config_path: Path
    _data_path: Path

    def _init_linux(self):
        self._data_path = xdg_data_home()

    def _init_windows(self):
        #self._config_path = Path(getenv("APPDATA", ""))
        self._data_path = Path(getenv("LOCALAPPDATA", ""))

    def _init_darwin(self):
        darwin_library = Path.home() / "Library"
        #self._config_path = darwin_library / "Preferences"
        self._data_path = darwin_library / "Application Support"

    def _init_portable(self):
        portable_data = Path.cwd() / PORTABLE_PREFIX
        self._data_path = portable_data / "data"

    @property
    def data_path(self):
        return self._data_path / APP_NAME

    def __init__(self):
        if getenv("PORTABLE_APP"):
            self._init_portable()
        elif sys.platform == "linux":
            self._init_linux()
        elif sys.platform == "darwin":
            self._init_darwin()
        elif sys.platform == "win32":
            self._init_windows()
        else:
            self._init_portable()


APPDIRS = AppDirs()
