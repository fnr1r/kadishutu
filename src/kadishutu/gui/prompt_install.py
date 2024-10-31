from enum import Enum, auto
import os
import sys
from kadishutu.tools.depinstall import get_install_handler
from kadishutu.tools.depinstall.poetry import PoetryInstallHandler
from typing import Callable, NoReturn


class Result(Enum):
    Success = 0
    Rejected = auto()


def cli_frontend(install_func: Callable[[], None]) -> Result:
    ans = input("Install GUI dependencies? [y/N]: ")
    if not ans.lower().startswith("y"):
        return Result.Rejected
    install_func()
    print("Done. Everything should work now.")
    return Result.Success


def tk_frontend(install_func: Callable[[], None]) -> Result:
    from tkinter import messagebox
    if not messagebox.askyesno(
        "kadishutu: Additional dependencies",
        "The GUI can't function without aditional dependencies. Do you want to install them?"
    ):
        return Result.Rejected
    try:
        install_func()
    except Exception as e:
        messagebox.showerror(
            "kadishutu",
            f"The following error has occured: {repr(e)}"
        )
        raise e
    messagebox.showinfo(
        "kadishutu",
        "Installed! The app should restart automatically."
    )
    return Result.Success


def reexec_self() -> NoReturn:
    os.execl(sys.executable, *sys.orig_argv)


def handle_no_qt() -> int:
    print("PySide6 is not installed.")
    try:
        handler = get_install_handler()
    except AssertionError:
        print("Please install it before running the gui.")
        return 1
    handler_frontend = tk_frontend
    if isinstance(handler, PoetryInstallHandler):
        handler_frontend = cli_frontend
    res = handler_frontend(lambda: handler.install_group("gui"))
    if res == Result.Success:
        reexec_self()
    return 1
