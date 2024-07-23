#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict

from .cli import (
    cmd_decrypt, cmd_encrypt, cmd_inspect, cmd_print, cmd_update_hash
)


def cmd_gui(args):
    from .gui import gui_main
    gui_main(args)


SUBPARSERS: Dict[str, ArgumentParser] = {}


def cmd_help(parser: ArgumentParser, args: Namespace):
    if not args.subcommand:
        parser.print_help()
    try:
        SUBPARSERS[args.subcommand].print_help()
    except KeyError:
        parser.print_help()


def main():
    parser = ArgumentParser()
    #parser.add_argument("command", nargs="+")
    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand", required=True)

    parser_decrypt = subparsers.add_parser("decrypt")
    parser_decrypt.add_argument("source", type=Path)
    parser_decrypt.add_argument("destination", type=Path)
    parser_decrypt.set_defaults(func=cmd_decrypt)
    SUBPARSERS["decrypt"] = parser_decrypt

    parser_encrypt = subparsers.add_parser("encrypt")
    parser_encrypt.add_argument("source", type=Path)
    parser_encrypt.add_argument("destination", type=Path)
    parser_encrypt.add_argument("--update-hash", type=bool)
    parser_encrypt.set_defaults(func=cmd_encrypt)
    SUBPARSERS["encrypt"] = parser_encrypt

    parser_gui = subparsers.add_parser("gui")
    parser_gui.add_argument("file", type=Path)
    parser_gui.set_defaults(func=cmd_gui)
    SUBPARSERS["gui"] = parser_gui

    parser_help = subparsers.add_parser("help")
    parser_help.add_argument("subcommand", type=str, nargs="?")
    parser_help.set_defaults(func=lambda x: cmd_help(parser, x))
    SUBPARSERS["help"] = parser_help

    parser_inspect = subparsers.add_parser("inspect")
    parser_inspect.add_argument("file", type=Path)
    parser_inspect.add_argument("selector", nargs="+")
    parser_inspect.add_argument("--ignore-hash", type=bool)
    parser_inspect.set_defaults(func=cmd_inspect)
    SUBPARSERS["inspect"] = parser_inspect

    parser_print = subparsers.add_parser("print")
    parser_print.add_argument("file", type=Path)
    parser_print.add_argument("--ignore-hash", type=bool)
    parser_print.set_defaults(func=cmd_print)
    SUBPARSERS["print"] = parser_print

    parser_update_hash = subparsers.add_parser("update_hash")
    parser_update_hash.add_argument("file", type=Path)
    parser_update_hash.set_defaults(func=cmd_update_hash)
    SUBPARSERS["update_hash"] = parser_update_hash

    args = parser.parse_args()

    args.func(args)