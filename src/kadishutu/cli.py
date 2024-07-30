import importlib
from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
from struct import Struct
from types import FunctionType, MethodType
from typing import Any, List

from .demons import Affinity, get_demon_name
from .file_handling import DecryptedSave, EncryptedSave
from .game import SaveEditor
from .innate_skills import get_innate_skill_name
from .skills import get_skill_name


def print_affinities(affinities: dict):
    print(" Affinities:")
    for (k, v) in affinities.items():
        print(" ", k, Affinity(v).name)


def print_potentials(potentials: dict):
    print(" Potentials:")
    for (k, v) in potentials.items():
        v = str(v)
        if v != "0" and not v.startswith("-"):
            v = "+" + v
        print(" ", k, v)


def print_skills(skills: dict):
    print(" Skills:")
    for i in range(1, 9):
        skill_id = skills[f"S{i}"]
        if not skill_id:
            break
        try:
            skill_name = get_skill_name(skill_id)
        except KeyError:
            skill_name = f"??? of id {skill_id}"
        print("  Skill {}: {} (mystery value: {})".format(
            i, skill_name, skills[f"unk{i}"]
        ))


def endswith_any(haystack: List[str], needle: str) -> bool:
    for kk in haystack:
        if needle.endswith(kk):
            return True
    return False


def verbose_print(save: SaveEditor):
    print("Player:")
    print(" Name:", save.player.first_name, save.player.last_name)
    print(" Play time:", save.play_time)
    print(" Macca:", save.macca)
    print(" Glory:", save.glory)
    #print_affinities(save.player.affinities)
    #print_potentials(save.data["potentials"])
    #print_skills(save.data["skills"])
    #print(save.data["stats_initial"])
    #print(save.data["stats_changes"])
    #print(save.data["stats_current"])
    for i in range(24):
        demon = save.demon(i)
        if demon.demon_id == 2**16 - 1:
            continue
        print(f"Demon {i}:")
        demon_id = demon.demon_id
        try:
            demon_name = f"{get_demon_name(demon_id)} (id {demon_id})"
        except KeyError:
            demon_name = f"??? of id {demon_id}"
        print(f" Name: {demon_name}")
        innate_skill_obj = demon.innate_skill
        try:
            innate_skill = f"{innate_skill_obj.name} (id {innate_skill_obj.id})"
        except KeyError:
            innate_skill = f"??? of id {innate_skill_obj.id}"
        print(" Innate skill:", innate_skill)
        #print_affinities(named("affinities"))
        #print_potentials(named("potentials"))
        #print_skills(named("skills"))
        #for k in keys:
        #    if endswith_any(["id", "innate_skill", "affinities", "potentials", "skills", "raw"], k):
        #        continue
        #    v = save.data[k]
        #    print("", k[len(base_name)+1:] + ":", v)


def cmd_print(args):
    path = args.file
    savefile = DecryptedSave.auto_open(path)
    if not savefile.hash_validate():
        if args.ignore_hash:
            print("The hash is invalid!")
        else:
            raise ValueError("The save file checksum does not match.")
    gamesave = SaveEditor(savefile)
    #import pprint
    #a = {}
    #for i in ["difficulty"]:
    #    i = i.format(id="12".zfill(2))
    #    a[i] = gamesave.data[i]
    #a = gamesave.data
    #pprint.pprint(a)
    #ts = Struct("<L").unpack_from(buf, 0x4f0)[0]
    #print(ts)
    #ts = a["time"]
    #ts = datetime.datetime.fromtimestamp(ts/1000.0)
    #print(ts.strftime('%Y-%m-%d %H:%M:%S'))
    #base_epoch = datetime.datetime(2024, 1, 1)
    #print(base_epoch + timedelta(minutes=ts))
    #print(gamesave.model_dump())
    verbose_print(gamesave)
    from .items import ItemTable, BUILTIN_ITEM_TABLE
    itable = ItemTable.from_dict({"items": BUILTIN_ITEM_TABLE})
    for i in itable.items:
        print("{}: {}/{} (id: {})".format(
            i.name,
            Struct("<B").unpack_from(savefile.data, i.offset)[0],
            i.get_limit(),
            i.id,
        ))


def cmd_decrypt(args):
    source = args.source
    if args.destination:
        destination = args.destination
    else:
        destination = source
    print(f"Opening {source}")
    savefile = EncryptedSave.open(source)
    assert not savefile.is_save_decrypted(), "Save file already decrypted"
    print("Decrypting...")
    savefile = savefile.decrypt()
    assert savefile.is_save_decrypted(), "Save file decryption failed"
    assert savefile.hash_validate(), "The save file's hash is not valid."
    print(f"Saving file to {destination}")
    savefile.save(destination)


def cmd_encrypt(args):
    source = args.source
    if args.destination:
        destination = args.destination
    else:
        destination = source
    print(f"Opening {source}")
    savefile = DecryptedSave.open(source)
    assert savefile.is_save_decrypted, "Save file already encrypted"
    if savefile.hash_validate():
        print("Contained hash is valid.")
    elif args.update_hash:
        print("Updating contained hash.")
        savefile.hash_update()
    else:
        raise ValueError("The save file's hash is not valid. Re-run with \"--update-hash\".")
    print(f"Saving file to {destination}")
    savefile.encrypt().save(destination)


def cmd_inspect(args):
    path = args.file
    savefile = DecryptedSave.auto_open(path)
    game = SaveEditor(savefile)
    this = game
    skip = 0
    # JaNkTaStIc!
    for i, txt in enumerate(args.selector):
        if skip:
            skip -= 1
            continue
        this = this.__getattribute__(txt)
        if isinstance(this, MethodType) or isinstance(this, FunctionType):
            arglist = this.__annotations__
            arglist.pop("return")
            skip = len(arglist)
            arglistd = []
            for k, v in enumerate(arglist.values()):
                tx = args.selector[i + k + 1]
                arglistd.append(v(tx))
            this = this(*arglistd)
            continue
    #if isinstance(this, property):
    #    this = this.getter()
    this: Any
    # NOTE: Currently broken for properties
    if hasattr(this, "offset"):
        print(f"Offset: 0x{this.offset:x}")
    #raise ValueError("Offset not available")
    print(this)


def cmd_run_script(args):
    path: Path = args.file
    script_path: Path = args.script.absolute()
    savefile = DecryptedSave.auto_open(path)
    #script = importlib.import_module(str(script_path))
    loader = SourceFileLoader("script", str(script_path))
    spec = importlib.util.spec_from_loader("script", loader)
    assert spec
    script = importlib.util.module_from_spec(spec)
    loader.exec_module(script)
    #if not hasattr(script, "main"):
    #    raise ValueError("The main function is not defined")
    #assert script.main
    #if not isinstance(script.main, FunctionType):
    #    raise ValueError("main is not a function")
    script.main(path, savefile, args.rest_of_args)


def cmd_update_hash(args):
    path = args.file
    savefile = DecryptedSave.open(path)
    if savefile.hash_validate():
        print("The hash is already valid.")
        return
    savefile.hash_update()
    savefile.save(path)
