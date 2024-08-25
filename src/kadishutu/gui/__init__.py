try:
    from PySide6 import __version__
except ImportError:
    from .prompt_install import handle_no_qt
    import sys
    sys.exit(handle_no_qt())

from .mainwindow import gui_main

__all__ = ["gui_main"]
