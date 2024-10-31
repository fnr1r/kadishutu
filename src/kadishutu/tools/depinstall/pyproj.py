from functools import cache
from kadishutu.encodings import ENCODING
import os
from pathlib import Path
import toml
from typing import Any, Dict


PYPROJ = "pyproject.toml"
THIS_DIR = Path(os.path.realpath(__file__)).parent
PYPROJECT = THIS_DIR / PYPROJ
OTHER_PYPROJECT = THIS_DIR / "../../../.." / PYPROJ


@cache
def get_pyproject_data() -> Dict[str, Any]:
    def tomlload(path):
        with open(path, "r", encoding=ENCODING) as file:
            return toml.load(file)
    from .poetry import PoetryInstallHandler
    if PoetryInstallHandler.likelyness() >= 90:
        try:
            return tomlload(OTHER_PYPROJECT)
        except FileNotFoundError:
            pass
    return tomlload(PYPROJECT)


def get_groups() -> Dict[str, Any]:
    pyproj = get_pyproject_data()
    return pyproj["tool"]["poetry"]["group"]


def get_opt_depends(group: str) -> Dict[str, Any]:
    return get_groups()[group]["dependencies"]
