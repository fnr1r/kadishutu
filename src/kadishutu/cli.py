import importlib
from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
from types import FunctionType, MethodType
from typing import Any

from kadishutu.core.shared.file_handling import DecryptedSave, EncryptedSave
from kadishutu.core.game_save import GameSaveEditor


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
    game = GameSaveEditor(savefile)
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
            try:
                arglist.pop("return")
            except KeyError:
                pass
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
