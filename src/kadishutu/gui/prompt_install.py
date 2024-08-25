from enum import Enum, auto
import os
from subprocess import Popen
import sys
from tkinter import messagebox
from typing import NoReturn


GUI_DEPS = ["pillow==10.4.0", "pyside6==6.7.2", "xdg==6.0.0"]


class Result(Enum):
    Success = 0
    NoCommand = auto()
    Rejected = auto()
    Errored = auto()


def command_exists(cmd: str) -> bool:
    try:
        Popen([cmd]).terminate()
    except FileNotFoundError:
        return False
    return True


def get_pipx_installed_name() -> str:
    # TODO
    return "kadishutu"


def poetry_install_handler() -> Result:
    if not command_exists("poetry"):
        return Result.NoCommand
    ans = input("Install GUI dependencies? [y/N]: ")
    if not ans.lower().startswith("y"):
        return Result.Rejected
    p = Popen(["poetry", "install", "--without", "dev", "--with", "gui"])
    p.wait()
    print("Done. Everything should work now.")
    return Result.Success


def pipx_install_handler() -> Result:
    if not command_exists("pipx"):
        return Result.NoCommand
    name = get_pipx_installed_name()
    if not messagebox.askyesno(
        "kadishutu: Additional dependencies",
        "The GUI can't function without aditional dependencies. Do you want to install them?"
    ):
        return Result.Rejected
    try:
        p = Popen(["pipx", "inject", name, *GUI_DEPS])
        p.wait()
    except Exception as e:
        messagebox.showerror(
            "kadishutu",
            f"The following error has occured: {e.__repr__()}"
        )
        return Result.Errored
    messagebox.showinfo(
        "kadishutu",
        "Installed! The app should restart automatically."
    )
    return Result.Success


def reexec_self() -> NoReturn:
    os.execl(sys.executable, *sys.orig_argv)


def handle_no_qt() -> int:
    print("PySide6 is not installed.")
    for condition, fun in [
        ("VIRTUAL_ENV" in os.environ, poetry_install_handler),
        ("pipx" in __file__, pipx_install_handler)
    ]:
        if not condition:
            continue
        res = fun()
        if res == Result.Success:
            reexec_self()
        elif res == Result.NoCommand:
            continue
        elif res in [Result.Rejected, Result.Errored]:
            return 1
    print("Please install it before running the gui.")
    return 1
