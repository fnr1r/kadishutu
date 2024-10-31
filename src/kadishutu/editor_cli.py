from argparse import ArgumentParser, Namespace
from math import floor
from pathlib import Path
from typing import Optional

from kadishutu.core.game_save import GameSaveEditor
from kadishutu.core.game_save.dlc import DlcBitflags
from kadishutu.core.game_save.game import DlcEditor
from kadishutu.core.shared.file_handling import (
    DecryptedSave, EncryptedSave, is_save_decrypted,
)


def dlc_clear(_: Namespace, dlc: DlcEditor):
    dlc.clear()


def dlc_print(_: Namespace, dlc: DlcEditor):
    print(dlc.get().get_flags())


def dlc_remove(args: Namespace, dlc: DlcEditor):
    name: str = args.name
    dlc.flags = dlc.flags & ~DlcBitflags.from_str(name)


def edit_dlc(args: Namespace, game: GameSaveEditor):
    args.func_y(args, game.dlc)


def edit_glory(args: Namespace, game: GameSaveEditor):
    value: Optional[int] = args.value
    if value is not None:
        game.glory = value
    else:
        print("Glory:", game.glory)


def edit_play_time(_: Namespace, game: GameSaveEditor):
    from datetime import timedelta
    time: timedelta = game.play_time
    seconds = int(time.total_seconds())
    hours = floor(seconds / 60 / 60)
    seconds -= hours * 60 * 60
    minutes = floor(seconds / 60)
    seconds -= minutes * 60
    game_display = f"{hours}:{minutes:02}:{seconds:02}"
    print("Play time:", game_display, "or", game.play_time)


def edit_macca(args: Namespace, game: GameSaveEditor):
    value: Optional[int] = args.value
    if value is not None:
        game.macca = value
    else:
        print("Macca:", game.macca)


def cmd_edit(args: Namespace):
    path = args.file
    with open(path, "rb") as f:
        data = bytearray(f.read())
    reencrypt = not is_save_decrypted(data)
    if reencrypt:
        file = EncryptedSave(data).decrypt()
    else:
        file = DecryptedSave(data)
    game = GameSaveEditor(file)
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

    glory = subparsers.add_parser("glory")
    glory.set_defaults(func_x=edit_glory)
    glory.add_argument("value", nargs="?", type=int)

    play_time = subparsers.add_parser("play_time")
    play_time.set_defaults(func_x=edit_play_time)

    macca = subparsers.add_parser("macca")
    macca.set_defaults(func_x=edit_macca)
    macca.add_argument("value", nargs="?", type=int)

    return parser
