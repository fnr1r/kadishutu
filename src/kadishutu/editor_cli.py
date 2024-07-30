from pathlib import Path
from argparse import ArgumentParser, Namespace

from .dlc import DlcBitflags
from .file_handling import DecryptedSave, EncryptedSave, is_save_decrypted
from .game import DlcEditor, SaveEditor


def dlc_clear(_: Namespace, dlc: DlcEditor):
    dlc.clear()


def dlc_print(_: Namespace, dlc: DlcEditor):
    print(dlc.get().get_flags())


def dlc_remove(args: Namespace, dlc: DlcEditor):
    name: str = args.name
    dlc.flags = dlc.flags & ~DlcBitflags.from_str(name)


def edit_dlc(args: Namespace, game: SaveEditor):
    args.func_y(args, game.dlc)


def cmd_edit(args: Namespace):
    path = args.file
    with open(path, "rb") as file:
        data = bytearray(file.read())
    reencrypt = not is_save_decrypted(data)
    if reencrypt:
        file = EncryptedSave(data).decrypt()
    else:
        file = DecryptedSave(data)
    game = SaveEditor(file)
    args.func_x(args, game)
    file.hash_update()
    if reencrypt:
        file.encrypt().save(path)
    else:
        file.save(path)


def argparse_edit(subparsers):
    parser: ArgumentParser = subparsers.add_parser("edit")
    assert isinstance(parser, ArgumentParser)
    parser.add_argument("file", type=Path)
    parser.set_defaults(func=cmd_edit)
    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand_x", required=True)

    dlc = subparsers.add_parser("dlc")
    dlc.set_defaults(func_x=edit_dlc)
    dlc_subp = dlc.add_subparsers(title="subcommand", dest="subcommand_y", required=True)

    dlc_clear_p = dlc_subp.add_parser("clear")
    dlc_clear_p.set_defaults(func_y=dlc_clear)

    dlc_print_p = dlc_subp.add_parser("print")
    dlc_print_p.set_defaults(func_y=dlc_print)

    dlc_remove_p = dlc_subp.add_parser("remove")
    dlc_remove_p.set_defaults(func_y=dlc_remove)
    dlc_remove_p.add_argument("name", type=str)

    return parser