from pathlib import Path
from tkinter import Button, Entry, Label, Menu, StringVar, Tk, Toplevel, filedialog
from tkinter.messagebox import showerror
from typing import Any, Callable, Optional
from typing_extensions import Self

from .file_handling import DecryptedSave
from .game import SaveEditor


# NOTE: Only valid after init
MAIN_WINDOW: "MainWindow" = None  # type: ignore


class TkX(Tk):
    __doc__ = Tk.__doc__

    def spawn(self, subwindow: Callable[[Self], Any]) -> Callable[[], None]:
        "Spawns a class with self as root"
        return lambda: subwindow(self)


class MutEntry(Entry):
    def __init__(self, *args, value: Optional[str] = None, **kwargs):
        print(value)
        super().__init__(*args, **kwargs)
        self.var = StringVar(self, value)
        self.config(textvariable=self.var)
        self.modified = False
        self.cbname = self.var.trace_add("write", self.set_modified)

    def set_modified(self, _: str, _2: str, mode: str):
        self.modified = True
        self.var.trace_remove("write", self.cbname)


class ProtagonistEditor(Toplevel):
    def __init__(self, root: "MainWindow"):
        super().__init__(root)
        row = 0
        Label(self, text="Name:").grid(column=0, row=row)
        self.protag_name = MutEntry(
            self,
            value=root.save.player.first_name,
            width=12
        )
        self.protag_name.grid(column=1, row=row)
        self.protag_surname = MutEntry(
            self,
            value=root.save.player.last_name,
            width=10
        )
        self.protag_surname.grid(column=2, row=row)
        row += 1
        Label(self, text="Macca:").grid(column=0, row=row)
        self.macca = MutEntry(
            self,
            value=str(root.save.macca),
            width=20
        )
        self.macca.grid(column=1, row=row)
        row += 1
        Label(self, text="Glory:").grid(column=0, row=row)
        self.glory = MutEntry(
            self,
            value=str(root.save.glory),
            width=20
        )
        self.glory.grid(column=1, row=row)
        row += 1
        Button(self, text="Save", command=self.save).grid(column=0, row=row)
        Button(self, text="Cancel", command=self.cancel).grid(column=1, row=row)

    def save(self):
        self.destroy()

    def cancel(self):
        self.destroy()


class DemonEditor(Toplevel):
    def __init__(self, root: "MainWindow"):
        try:
            demon_number = int(root.demon_number.get())
            if demon_number < 0 or demon_number > 2:
                raise ValueError
        except ValueError:
            # Fixes returning early
            demon_number = None
        super().__init__(root)
        if not demon_number:
            self.destroy()
            showerror(
                message="Bad demon number. Enter from 0-23."
            )
            return
        row = 0
        #self.
        return


class MenuBar(Menu):
    def __init__(self, root: "MainWindow"):
        super().__init__()
        self.file_menu = Menu(self)
        self.file_menu.add_command(
            label="Open",
            command=root.open_file,
        )
        self.file_menu.add_command(
            label="Save (encrypted)",
            command=root.save_file_encrypted,
        )
        self.file_menu.add_command(
            label="Save (decrypted)",
            command=root.save_file_decrypted,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit",
            command=root.destroy,
        )
        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )


class MainWindow(TkX):
    path: Optional[Path] = None
    raw: Optional[DecryptedSave] = None

    def __init__(self):
        super().__init__()
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)
        Label(self, text="Path:").grid(column=0, row=0)
        self.path_label = Label(text="")
        self.path_label.grid(column=1, row=0)
        Button(
            self,
            text="Edit Protagonist",
            command=self.spawn(ProtagonistEditor)
        ).grid(column=0, row=1)
        Button(
            self,
            text="Edit Demon",
            command=self.spawn(DemonEditor)
        ).grid(column=0, row=2)
        self.demon_number = Entry(
            self,
            width=2
        )
        self.demon_number.grid(column=1, row=2)

    def reload_file(self):
        if not self.path:
            return
        self.raw = DecryptedSave.auto_open(self.path)
        self.save = SaveEditor(self.raw)
        self.path_label.config(text=self.path.name)

    def open_file(self):
        path = filedialog.askopenfilename(title="Open GameSaveXX")
        if not path:
            return
        self.path = Path(path)
        self.reload_file()

    def save_file_encrypted(self):
        if not self.path:
            showerror(
                message="No file open"
            )
            return
        assert self.raw
        self.raw.hash_update()
        self.raw.encrypt().save(self.path)

    def save_file_decrypted(self):
        if not self.path:
            showerror(
                message="No file open"
            )
            return
        assert self.raw
        self.raw.hash_update()
        self.raw.encrypt().save(self.path)


def gui_main(args):
    MAIN_WINDOW = MainWindow()
    if args.file:
        MAIN_WINDOW.path = args.file
        MAIN_WINDOW.reload_file()
    MAIN_WINDOW.mainloop()
