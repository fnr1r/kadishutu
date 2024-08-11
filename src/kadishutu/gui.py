from abc import ABC, abstractmethod
from pathlib import Path
from tkinter import BooleanVar, Canvas, IntVar, Menu, StringVar, Tk, Toplevel, Variable, filedialog
from tkinter.messagebox import showerror
from tkinter.ttk import Button, Checkbutton, Combobox, Entry, Frame, Label, Notebook, Scrollbar
from _tkinter import TclError
from tktooltip import ToolTip
from typing import Any, Callable, Dict, List, Optional, Tuple

from .alignment import AlignmentEditor, AlignmentManager
from .data.alignment import ALIGNMENT_OFFSET_MAP, AlignmentByte
from .data.demons import DEMON_ID_MAP, DEMON_NAME_MAP, DEMONS
from .data.essences import ESSENCE_OFFSETS
from .data.items import CONSUMABLES_RANGE, Item, items_from
from .data.skills import NEW_SKILLS, SKILL_NAME_MAP
from .demons import AFFINITY_MAP, AFFINITY_NAMES, STATS_NAMES, Affinity, AffinityEditor, DemonEditor, PType, PotentialEditor, StatsEditor
from .dlc import DlcBitflags
from .essences import ESSENCE_META_MAP, EssenceManager, EssenceMetadata
from .file_handling import DecryptedSave, EncryptedSave, is_save_decrypted
from .game import SaveEditor
from .items import ItemManager
from .player import NameManager
from .skills import SKILL_ID_MAP, Skill, SkillEditor


# NOTE: Only valid after init
MAIN_WINDOW: "MainWindow" = None  # type: ignore


class SpawnerMixin(ABC):
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


class MutEntry(Entry, MutabilityMixin):
    def __init__(self, *args, value: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = StringVar(self, value)
        self.config(textvariable=self.var)
        MutabilityMixin.__init__(self)

    def get(self) -> str:
        return self.var.get()


class NameEditorTk(Frame):
    NAMES = [
        "save_name", "first_name", "last_name", "first_name_again",
        "combined_name"
    ]
    UF_NAMES = [
        "Save name", "First name", "Last name", "First name again",
        "Combined name"
    ]

    def __init__(self, *args, names: NameManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = names
        self.named: dict[str, MutEntry] = {}

        f = Frame(self)
        Label(f, text="Extend name length", width=20).pack(side="left")
        self.limit_switch = MutCheckbutton(f, command=self._limit)
        self.limit_switch.pack(side="left")
        f.pack(expand=True, fill="x")

        for name, uf_name in zip(self.NAMES, self.UF_NAMES):
            f = Frame(self)
            Label(f, text=uf_name + ": ", width=16).pack(side="left")
            value: str = names.__getattribute__(name).get()
            namebox = MutEntry(f, value=value)
            namebox.pack(side="left")
            f.pack(expand=True, fill="x")
            self.named[name] = namebox

        Button(self, text="Save", command=self.save).pack()

    def _limit(self):
        self.obj.over_limit = self.limit_switch.get()

    def save(self):
        for k, v in self.named.items():
            if not v.modified:
                continue
            self.obj.__getattribute__(k).set(v.get())


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
    @classmethod
    @abstractmethod
    def name_list(cls) -> List[str]: ...

    @classmethod
    @abstractmethod
    def id_to_name(cls, id: int) -> str: ...

    @classmethod
    @abstractmethod
    def name_to_id(cls, name: str) -> int: ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = MutInt(self)
        self.id.trace_add("write", self.update_name)
        self.id.grid(column=0, row=0)
        self.name = MutCombobox(self, values=self.name_list())
        self.name.trace_add("write", self.update_id)
        self.name.grid(column=1, row=0)

    def update_name(self, _: str, _2: str, _3: str):
        try:
            id = self.id.get()
            name = self.id_to_name(id)
        except TclError:
            return
        except KeyError:
            return
        self.name.set(name)

    def update_id(self, _: str, _2: str, _3: str):
        try:
            name = self.name.get()
            id = self.name_to_id(name)
        except TclError:
            return
        except IndexError:
            return
        self.id.set(id)


class SkillCombox(IdCombox):
    SKILL_NAMES = [
        skill.name
        for skill in NEW_SKILLS
    ]
    @classmethod
    def name_list(cls) -> List[str]:
        return cls.SKILL_NAMES
    @classmethod
    def id_to_name(cls, id: int) -> str:
        return SKILL_ID_MAP[id].name
    @classmethod
    def name_to_id(cls, name: str) -> int:
        return SKILL_NAME_MAP[name].id


class SkillEditorTk(Frame):
    def __init__(self, *args, innate_skill: Skill, skills: SkillEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.innate_skill = innate_skill
        self.obj = skills
        self.skilld: List[Tuple[SkillCombox, MutInt]] = []

        Label(self, text=f"Innate skill:").grid(column=0, row=0)
        self.innate_skill_box = SkillCombox(self)
        self.innate_skill_box.id.set(innate_skill.id)
        self.innate_skill_box.grid(column=1, row=0)

        for i in range(0, 8):
            row = i + 1
            Label(self, text=f"Skill {i + 1}:").grid(column=0, row=row)
            skill = skills.slot(i)
            skillbox = SkillCombox(self)
            skillbox.id.set(skill.id)
            skillbox.grid(column=1, row=row)
            mysterybox = MutInt(self, value=skill._unknown)
            mysterybox.grid(column=2, row=row)
            self.skilld.append((skillbox, mysterybox))

        row += 1

        Button(self, text="Save", command=self.save).grid(column=0, row=row)

    def save(self):
        if self.innate_skill_box.id.modified:
            self.innate_skill.id = self.innate_skill_box.id.get()
        for i, (skillbox, mysterybox) in enumerate(self.skilld):
            skill = self.obj.slot(i)
            if skillbox.id.modified:
                skill.id = skillbox.id.get()
            if mysterybox.modified:
                skill._unknown = mysterybox.get()


class AffinityEditorTk(Frame):
    def __init__(self, *args, affinities: AffinityEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = affinities
        self.affinityd: dict[str, MutCombobox] = {}

        for i in AFFINITY_NAMES:
            f = Frame(self)
            Label(f, text=i, width=16).pack(side="left")
            i = i.lower()
            affinity: Affinity = affinities.__getattribute__(i)
            affinitybox = MutCombobox(f, value=affinity.name, values=list(AFFINITY_MAP.keys()))
            affinitybox.pack(side="left")
            f.pack(expand=True, fill="x")
            self.affinityd[i] = affinitybox

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        for k, v in self.affinityd.items():
            if not v.modified:
                continue
            affinity = AFFINITY_MAP[v.get()]
            self.obj.__setattr__(k, affinity)


class PotentialEditorTk(Frame):
    def __init__(self, *args, potentials: PotentialEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = potentials
        self.potentiald: dict[PType, MutInt] = {}

        for i in PType:
            f = Frame(self)
            Label(f, text=i.name).pack(side="left")
            potential: int = potentials.__getattribute__(i.name.lower())
            potentialbox = MutInt(f, value=potential)
            potentialbox.pack(side="left")
            f.pack(expand=True, fill="x")
            self.potentiald[i] = potentialbox

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        for k, v in self.potentiald.items():
            if not v.modified:
                continue
            self.obj.__setattr__(k.name.lower(), v.get())


class PlayerEditorTk(Toplevel):
    master: "MainWindow"

    def __init__(self, master: "MainWindow", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.obj = master.save.player
        self.tabbed = Notebook(self)
        self.tabbed.pack()
        general = Frame(self.tabbed)
        row = 0
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
        self.tabbed.add(NameEditorTk(self, names=self.obj.names), text="Names")
        self.tabbed.add(StatEditorTk(self, stats=self.obj.stats), text="Stats")
        self.tabbed.add(SkillEditorTk(self, innate_skill=self.obj.innate_skill, skills=self.obj.skills), text="Skills")
        self.tabbed.add(AffinityEditorTk(self, affinities=self.obj.affinities), text="Affinities")
        self.tabbed.add(PotentialEditorTk(self, potentials=self.obj.potentials), text="Potentials")

    def save(self):
        if self.macca.modified:
            self.master.save.glory = self.macca.get()
        if self.glory.modified:
            self.master.save.glory = self.glory.get()


class DemonIdCombox(IdCombox):
    DEMON_NAMES = [
        demon["name"]
        for demon in DEMONS
    ]
    @classmethod
    def name_list(cls) -> List[str]:
        return cls.DEMON_NAMES
    @classmethod
    def id_to_name(cls, id: int) -> str:
        return DEMON_ID_MAP[id]["name"]
    @classmethod
    def name_to_id(cls, name: str) -> int:
        return DEMON_NAME_MAP[name]["id"]


class DemonEditorTk(Toplevel):
    def __init__(self, *args, demon: DemonEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = demon
        self.tabbed = Notebook(self)
        self.tabbed.pack()
        general = Frame(self.tabbed)
        row = 0
        Label(general, text="ID:").grid(column=0, row=row)
        self.demon_id = DemonIdCombox(general)
        self.demon_id.id.set(self.obj.demon_id)
        self.demon_id.grid(column=1, row=row)
        row += 1
        Button(general, text="Save", command=self.save).grid(column=0, row=row)
        self.tabbed.add(general, text="General")
        self.tabbed.add(StatEditorTk(self, stats=self.obj.stats), text="Stats")
        self.tabbed.add(SkillEditorTk(self, innate_skill=self.obj.innate_skill, skills=self.obj.skills), text="Skills")
        self.tabbed.add(AffinityEditorTk(self, affinities=self.obj.affinities), text="Affinities")
        self.tabbed.add(PotentialEditorTk(self, potentials=self.obj.potentials), text="Potentials")

    def save(self):
        if self.demon_id.id.modified:
            self.obj.demon_id = self.demon_id.id.get()


class VerticalScrolledFrame(Frame):
    def __init__(self, *args, width: Optional[int] = None, height: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.pack(fill="y", side="right", expand=False)
        self.canvas = Canvas(
            self, bd=0, highlightthickness=0, width=500, height=600,
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
    def __init__(self, *args, items: ItemManager, item_list: List[Item], **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = items
        self.itemd: Dict[int, MutInt] = {}

        self.list = VerticalScrolledFrame(self)
        self.list.pack()

        for item in item_list:
            f = Frame(self.list.inner)
            item = items.at_offset(item.offset, item_meta=item)
            txt = Label(f, text=item.name, width=24)
            desc = item.item_meta.desc
            if desc is not None:
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


class EssenceList(Frame):
    def __init__(self, *args, essences: EssenceManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = essences
        self.essenced: Dict[int, Tuple[MutCheckbutton, MutInt]] = {}

        self.list = VerticalScrolledFrame(self)
        self.list.pack()

        f = Frame(self.list.inner)
        Label(f, text="Essence", width=19).pack(anchor="e", expand=True, fill="x", side="left")
        Label(f, text="Ever owned?", width=20).pack(anchor="e", expand=True, fill="x", side="left")
        Label(f, text="Meta", width=20).pack(anchor="e", expand=True, fill="x", side="left")
        f.pack(expand=True, fill="x")

        for i in ESSENCE_OFFSETS:
            offset: int = i["offset"]
            name: str = i["name"]
            f = Frame(self.list.inner)
            essence = essences.at_offset(offset)
            txt = Label(f, text=name, width=24)
            txt.pack(side="left")
            ever_owned = MutCheckbutton(f, value=essence.amount > 0)
            ever_owned.pack(side="left")
            #try:
            #    value = EssenceMetadata(essence.metadata).name
            #except:
            #    value = ""
            #meta = MutCombobox(f, value=value, values=list(ESSENCE_META_MAP.keys()), width=20)
            meta = MutInt(f, value=essence.metadata, width=20)
            meta.pack(side="right")
            #meta = MutInt(f, value=essence.metadata.value, width=20)
            #meta.pack(side="right")
            self.essenced[essence.offset] = (ever_owned, meta)
            f.pack(expand=True, fill="x")

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        for k, (ever_owned, meta) in self.essenced.items():
            essence = self.obj.at_offset(k)
            if ever_owned.modified:
                essence.amount = int(ever_owned.get())
            if meta.modified:
                #essence.metadata = ESSENCE_META_MAP[meta.get()]
                essence.metadata = meta.get()


class ItemEditorTk(Toplevel, SpawnerMixin):
    def __init__(self, *args, items: ItemManager, essences: EssenceManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = items

        self.tabbed = Notebook(self)
        self.tabbed.pack()
        consumable_item_list = items_from(CONSUMABLES_RANGE)
        self.consumables = ItemList(self.tabbed, items=items, item_list=consumable_item_list)
        self.tabbed.add(self.consumables, text="Consumables")
        try:
            self.essences = EssenceList(self.tabbed, essences=essences)
        except ValueError as e:
            showerror("Internal error",
                "An internal error occured.\nPlease report this to the maintainer.\n{}"
                .format(
                    str(e),
                ))
        else:
            self.tabbed.add(self.essences, text="Essences")


class AlignmentFlagEditorTk(Frame):
    def __init__(self, *args, alignment: AlignmentEditor, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = alignment
        self.flagd: Dict[int, MutCheckbutton] = {}
        
        for bit in self.schema.bits:
            f = Frame(self)
            Label(f, text=f"Alignment: {bit.alignment}", width=16).pack(side="left")
            Label(f, text=f"Place: {bit.place}", width=20).pack(side="left")
            if bit.side_quest:
                Label(f, text=f"Quest: {bit.side_quest}").pack(side="left")
            f.pack(expand=True, fill="x")
            f = Frame(self)
            Label(f, text="\n".join(bit.text)).pack(side="left")
            button = MutCheckbutton(f, value=alignment[bit.bit])
            button.pack(side="left", padx=8)
            f.pack(expand=True, fill="x")
            self.flagd[bit.bit] = button

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        for bit, checkbutton in self.flagd.items():
            if not checkbutton.modified:
                continue
            self.obj.set_flag(bit, checkbutton.get())

    @property
    def schema(self) -> AlignmentByte:
        assert self.obj.schema
        return self.obj.schema


class AlignmentEditorTk(Toplevel):
    def __init__(self, *args, alignment: AlignmentManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = alignment
        self.tabbed = Notebook(self)
        self.tabbed.pack()
        for offset in ALIGNMENT_OFFSET_MAP:
            ooo = AlignmentFlagEditorTk(self.tabbed, alignment=alignment[offset])
            self.tabbed.add(ooo, text=f"0x{offset:5x}")


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
            command=self.spawner(ItemEditorTk, items=self.save.items, essences=self.save.essences)
        ).grid(column=0, row=row)
        Button(
            self,
            text="Edit Alignment",
            command=self.spawner(AlignmentEditorTk, alignment=self.save.alignment)
        ).grid(column=1, row=row)

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
