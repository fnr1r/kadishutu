from functools import cache
import os
from typing import List, Type

from .generic_early import InstallHandler
from .pipx import PipxInstallHandler
from .poetry import PoetryInstallHandler


INSTALL_HANDLERS: List[Type[InstallHandler]] = [
    PipxInstallHandler, PoetryInstallHandler,
]


@cache
def get_install_handler() -> InstallHandler:
    try:
        handler_var = os.environ["KADISHUTU_INSTALL_HANDLER"]
        if handler_var == "":
            raise KeyError
    except KeyError:
        pass
    else:
        for handler in INSTALL_HANDLERS:
            if handler.IDENT != handler_var:
                continue
            return handler()
        raise ValueError("Invalid install handler")
    selected = None
    largest_likelyness = 0
    for handler in INSTALL_HANDLERS:
        likelyness = handler.likelyness()
        if likelyness > largest_likelyness:
            largest_likelyness = likelyness
            selected = handler
    assert selected is not None
    return selected()
