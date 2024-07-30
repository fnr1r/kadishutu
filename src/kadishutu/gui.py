from abc import ABC
from pathlib import Path
from tkinter import BooleanVar, Canvas, IntVar, Menu, StringVar, Tk, Toplevel, Variable, filedialog
from tkinter.messagebox import showerror
from tkinter.ttk import Button, Checkbutton, Combobox, Entry, Frame, Label, Notebook, Scrollbar
from _tkinter import TclError
from tktooltip import ToolTip
from typing import Any, Callable, Dict, List, Optional, Tuple


from .data.demons import DEMONS
from .data.items import BUILTIN_ITEM_TABLE, ITEM_TABLE_OFFSET
from .data.skills import SKILLS
from .demons import STATS_NAMES, DemonEditor, StatsEditor
from .dlc import DlcBitflags
from .file_handling import DecryptedSave, EncryptedSave, is_save_decrypted
from .game import SaveEditor
from .items import ItemManager
from .skills import SkillEditor


# NOTE: Only valid after init
MAIN_WINDOW: "MainWindow" = None  # type: ignore


class SpawnerMixin:
    def spawner(self, subwindow: Callable[..., Any], *args, **kwargs) -> Callable[[], None]:
        "Spawns a class with self as master"
        return lambda: subwindow(self, *args, **kwargs)


class MutabilityMixin(ABC):
    var: Variable
    modified: bool
    callback_name: str

    def __init__(self):
        assert self.var
        self.modified = False
        self.callback_name = self.var.trace_add("write", self.set_modified)

    def set(self, *args, **kwargs):
        return self.var.set(*args, **kwargs)

    def trace_add(self, *args, **kwargs):
        return self.var.trace_add(*args, **kwargs)

    def set_modified(self, _: str, _2: str, _3: str):
        self.modified = True
        self.var.trace_remove("write", self.callback_name)


class MutCheckbutton(Checkbutton, MutabilityMixin):
    def __init__(self, *args, value: Optional[bool] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = BooleanVar(self, value)
        self.config(variable=self.var)
        MutabilityMixin.__init__(self)

    def get(self) -> bool:
        return self.var.get()


class DlcEditorTk(Toplevel):
    dlcmap: Dict[int, MutCheckbutton]

    def __init__(self, root: "MainWindow"):
        super().__init__(root)
        self.obj = root.save.dlc
        row = 0
        self.dlcmap = {}
        dlcs = self.obj.get()
        for i in DlcBitflags.all():
            name = i.get_flags()[0]
            Label(self, text=name).grid(column=0, row=row)
            button = MutCheckbutton(self, value=dlcs & DlcBitflags(i) != 0)
            button.grid(column=1, row=row)
            self.dlcmap[i] = button
            row += 1
        Button(self, text="Save", command=self.save).grid(column=0, row=row)
        Button(self, text="Cancel", command=self.cancel).grid(column=1, row=row)

    def save(self):
        res = DlcBitflags(0)
        for (k, v) in self.dlcmap.items():
            if v.get():
                res |= k
        print(res)
        self.obj.set(res)
        self.destroy()

    def cancel(self):
        self.destroy()


class MutEntry(Entry, MutabilityMixin):
    def __init__(self, *args, value: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = StringVar(self, value)
        self.config(textvariable=self.var)
        MutabilityMixin.__init__(self)

    def get(self) -> str:
        return self.var.get()


class MutInt(Entry, MutabilityMixin):
    def __init__(self, *args, value: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = IntVar(self, value)
        self.config(textvariable=self.var)
        MutabilityMixin.__init__(self)

    def get(self) -> int:
        return self.var.get()


class StatEditorTk(Frame):
    STYPES = ["Base", "Changes", "Current"]

    def __init__(self, *args, stats: StatsEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = stats
        self.statd: Dict[str, Dict[str, MutInt]] = {}

        row = 0
        column = 1
        for i in self.STYPES:
            Label(self, text=i).grid(column=column, row=row)
            i = i.lower()
            self.statd[i] = {}
            column += 1
        row += 1
        for i in STATS_NAMES:
            Label(self, text=i + ":").grid(column=0, row=row)
            i = i.lower()
            column = 1
            for j in self.STYPES:
                j = j.lower()
                value = self.obj.__getattribute__(j).__getattribute__(i)
                statvalue = MutInt(self, value=value, width=5)
                statvalue.grid(column=column, row=row)
                self.statd[j][i] = statvalue
                column += 1
            row += 1
        row += 1

        Button(self, text="Save", command=self.save).grid(column=0, row=row)

    def save(self):
        for j in STATS_NAMES:
            j = j.lower()
            for i in self.STYPES:
                i = i.lower()
                statvalue = self.statd[i][j]
                if not statvalue.modified:
                    continue
                self.obj.__getattribute__(i).__setattr__(j, statvalue.get())


class MutCombobox(Combobox, MutabilityMixin):
    def __init__(self, *args, value: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = StringVar(self, value)
        self.config(textvariable=self.var)
        MutabilityMixin.__init__(self)

    def get(self) -> str:
        return self.var.get()


class IdCombox(Frame):
    """
    Życie jest jak pudełko z kombosami - nigdy nie wiesz, co ci się przytrafi.

    \\-  Niekryty Krytyk udający Brucea Lee
    """

    def __init__(self, *args, idmap: Dict[int, str], **kwargs):
        super().__init__(*args, **kwargs)
        self.idmap = idmap
        self.id = MutInt(self)
        self.id.trace_add("write", self.update_name)
        self.id.grid(column=0, row=0)
        self.name = MutCombobox(self, values=list(idmap.values()))
        self.name.trace_add("write", self.update_id)
        self.name.grid(column=1, row=0)

    def update_name(self, _: str, _2: str, _3: str):
        try:
            id = self.id.get()
            name = self.idmap[id]
        except TclError:
            return
        except KeyError:
            return
        self.name.set(name)

    def update_id(self, _: str, _2: str, _3: str):
        try:
            name = self.name.get()
            id = [k for k, v in self.idmap.items() if v == name][0]
        except TclError:
            return
        except IndexError:
            return
        self.id.set(id)


class SkillEditorTk(Frame):
    def __init__(self, *args, skills: SkillEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = skills
        self.skilld: List[Tuple[IdCombox, MutInt]] = []

        for i in range(8):
            Label(self, text=f"Skill {i + 1}:").grid(column=0, row=i)
            skill = skills.slot(i)
            skillbox = IdCombox(self, idmap=SKILLS)
            skillbox.id.set(skill.id)
            skillbox.grid(column=1, row=i)
            mysterybox = MutInt(self, value=skill._unknown)
            mysterybox.grid(column=2, row=i)
            self.skilld.append((skillbox, mysterybox))

        row = i + 1

        Button(self, text="Save", command=self.save).grid(column=0, row=row)

    def save(self):
        for i, (skillbox, mysterybox) in enumerate(self.skilld):
            skill = self.obj.slot(i)
            if skillbox.id.modified:
                skill.id = skillbox.id.get()
            if mysterybox.modified:
                skill._unknown = mysterybox.get()


class PlayerEditorTk(Toplevel):
    def __init__(self, master: "MainWindow", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.obj = master.save.player
        self.tabbed = Notebook(self)
        self.tabbed.pack()
        general = Frame(self.tabbed)
        row = 0
        Label(general, text="Name:").grid(column=0, row=row)
        self.protag_name = MutEntry(
            general,
            value=self.obj.first_name,
            width=12
        )
        self.protag_name.grid(column=1, row=row)
        self.protag_surname = MutEntry(
            general,
            value=self.obj.last_name,
            width=10
        )
        self.protag_surname.grid(column=2, row=row)
        row += 1
        Label(general, text="Macca:").grid(column=0, row=row)
        self.macca = MutInt(
            general,
            value=master.save.macca,
            width=20
        )
        self.macca.grid(column=1, row=row)
        row += 1
        Label(general, text="Glory:").grid(column=0, row=row)
        self.glory = MutInt(
            general,
            value=master.save.glory,
            width=20
        )
        self.glory.grid(column=1, row=row)
        row += 1
        Button(general, text="Save", command=self.save).grid(column=0, row=row)
        self.tabbed.add(general, text="General")
        self.tabbed.add(StatEditorTk(self, stats=self.obj.stats), text="Stats")
        self.tabbed.add(SkillEditorTk(self, skills=self.obj.skills), text="Skills")

    def save(self):
        if self.macca.modified:
            MAIN_WINDOW.save.glory = self.macca.get()
        if self.glory.modified:
            MAIN_WINDOW.save.glory = self.glory.get()


class DemonEditorTk(Toplevel):
    def __init__(self, *args, demon: DemonEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = demon
        self.tabbed = Notebook(self)
        self.tabbed.pack()
        general = Frame(self.tabbed)
        row = 0
        Label(general, text="ID:").grid(column=0, row=row)
        self.demon_id = IdCombox(
            general,
            idmap=DEMONS
        )
        self.demon_id.id.set(self.obj.demon_id)
        self.demon_id.grid(column=1, row=row)
        row += 1
        Button(general, text="Save", command=self.save).grid(column=0, row=row)
        self.tabbed.add(general, text="General")
        self.tabbed.add(StatEditorTk(self, stats=self.obj.stats), text="Stats")
        self.tabbed.add(SkillEditorTk(self, skills=self.obj.skills), text="Skills")

    def save(self):
        if self.demon_id.id.modified:
            self.obj.demon_id = self.demon_id.id.get()


class VerticalScrolledFrame(Frame):
    def __init__(self, *args, width: Optional[int] = None, height: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.pack(fill="y", side="right", expand=False)
        self.canvas = Canvas(
            self, bd=0, highlightthickness=0, height=500,
            yscrollcommand=scrollbar.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.canvas.yview)
        self.inner = Frame(self.canvas)
        #self.inner.bind('<Enter>', self._bound_to_mousewheel)
        #self.inner.bind('<Leave>', self._unbound_to_mousewheel)
        #self.inner.bind("<Configure>", self._configure_inner)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.inner_id = self.canvas.create_window(0, 0, window=self.inner, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    #def _configure_inner(self, _):
    #    size = (self.inner.winfo_reqwidth(), self.inner.winfo_reqheight())
    #    self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
    #    if self.inner.winfo_reqwidth() != self.inner.winfo_width():
    #        self.inner.config(width=self.inner.winfo_reqwidth())

    def _configure_canvas(self, _):
        #if self.inner.winfo_reqwidth() != self.canvas.winfo_reqwidth():
        #    self.canvas.itemconfigure(self.inner_id, width=self.canvas.winfo_width())
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    #def _bound_to_mousewheel(self, event):
    #    self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    #def _unbound_to_mousewheel(self, event):
    #    self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class ItemList(Frame):
    def __init__(self, *args, items: ItemManager, itemsx: list[dict[str, Any]], **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = items
        self.itemd: Dict[int, MutInt] = {}

        self.list = VerticalScrolledFrame(self)
        self.list.pack()

        for i in itemsx:
            id: int = i["id"]
            name: str = i["name"]
            f = Frame(self.list.inner)
            item = items.at_offset(ITEM_TABLE_OFFSET + id)
            txt = Label(f, text=name, width=24)
            try:
                desc: str = i["desc"]
            except KeyError:
                pass
            else:
                ToolTip(txt, msg=desc, delay=1)
            txt.pack(anchor="e", expand=True, fill="x", side="left")
            Label(f, text="Limit: " + str(item.limit), width=16).pack(side="right", padx=4)
            amount = MutInt(f, value=item.amount, width=10)
            amount.pack(side="right")
            self.itemd[item.offset] = amount
            f.pack(expand=True, fill="x")

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        for k, v in self.itemd.items():
            if not v.modified:
                continue
            item = self.obj.at_offset(k)
            item.amount = v.get()


class ItemEditorTk(Toplevel, SpawnerMixin):
    def __init__(self, *args, items: ItemManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = items

        self.tabbed = Notebook(self)
        self.tabbed.pack()
        self.consumables = ItemList(self.tabbed, items=items, itemsx=BUILTIN_ITEM_TABLE)
        self.tabbed.add(self.consumables, text="Consumables")


class MenuBar(Menu):
    def __init__(self, master: "MainWindow", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_menu = Menu(self)
        self.file_menu.add_command(
            label="Open",
            command=master.file_open,
        )
        self.file_menu.add_command(
            label="Save",
            command=master.file_save,
        )
        self.file_menu.add_command(
            label="Save as",
            command=master.file_save_as,
        )
        self.file_menu.add_command(
            label="Reload",
            command=master.file_reload,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit",
            command=master.destroy,
        )
        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )


class MainWindow(Tk, SpawnerMixin):
    path: Path
    raw: DecryptedSave
    save: SaveEditor
    encrypted: BooleanVar

    def __init__(self, path: Optional[Path] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Kadishutu GUI (Tk)")
        row = 0
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)
        Label(self, text="Path:").grid(column=0, row=row)
        self.path_label = Label(text="")
        self.path_label.grid(column=1, row=row)
        row += 1
        Label(self, text="Encrypted:").grid(column=0, row=row)
        self.encrypted = BooleanVar(self)
        Checkbutton(self, variable=self.encrypted).grid(column=1, row=row)
        row += 1

        if path:
            self.path = path
            self.file_reload()
        else:
            self.file_open()
            assert self.path
        assert self.raw

        Button(
            self,
            text="Edit DLC",
            command=self.spawner(DlcEditorTk)
        ).grid(column=0, row=row)
        Button(
            self,
            text="Edit Player",
            command=self.spawner(PlayerEditorTk)
        ).grid(column=1, row=row)
        row += 1
        Button(
            self,
            text="Edit Demon",
            command=self.spawn_demon
        ).grid(column=0, row=row)
        self.demon_number = MutEntry(
            self,
            value="0",
            width=2
        )
        self.demon_number.grid(column=1, row=row)
        row += 1
        Button(
            self,
            text="Edit Items",
            command=self.spawner(ItemEditorTk, items=self.save.items)
        ).grid(column=0, row=row)

    def spawn_demon(self):
        try:
            demon_number = int(self.demon_number.get())
            if demon_number < 0 or demon_number > 29:
                raise ValueError
        except ValueError:
            showerror(
                message="Bad demon number. Enter from 0-29."
            )
        demon = self.save.demon(demon_number)
        DemonEditorTk(self, demon=demon)

    def file_reload(self):
        data = bytearray(self.path.read_bytes())
        encrypted = not is_save_decrypted(data)
        if encrypted:
            self.raw = EncryptedSave(data).decrypt()
        else:
            self.raw = DecryptedSave(data)
        self.save = SaveEditor(self.raw)
        self.path_label.config(text=self.path.name)
        self.encrypted.set(encrypted)

    def file_open(self):
        path = filedialog.askopenfilename(title="Open GameSaveXX")
        if not path:
            return
        self.path = Path(path)
        self.file_reload()

    def file_save(self):
        self.raw.hash_update()
        if self.encrypted.get():
            self.raw.encrypt().save(self.path)
        else:
            self.raw.save(self.path)

    def file_save_as(self):
        path_s = filedialog.asksaveasfilename(title="Target")
        if not path_s:
            return
        path = Path(path_s)
        self.raw.hash_update()
        if self.encrypted.get():
            self.raw.encrypt().save(path)
        else:
            self.raw.save(path)


def gui_main(args):
    MAIN_WINDOW = MainWindow(args.file)
    MAIN_WINDOW.mainloop()
