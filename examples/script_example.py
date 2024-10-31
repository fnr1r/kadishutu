# flake8: noqa: F402
# Ignore "module level import not at top of file" error

# SELF-REEXEC HEADER
# DO NOT EDIT
from pathlib import Path
from typing import NoReturn


def run_through_kadishutu() -> NoReturn:
    from argparse import ArgumentParser
    import os
    import sys
    parser = ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    script = sys.argv[0]
    file: Path = args.file
    os.execlp("kadishutu", "kadishutu", "run_script", script, str(file))


if __name__ == "__main__":
    run_through_kadishutu()
# EDIT FROM HERE


from typing import List

from kadishutu import DecryptedSave, GameSaveEditor


def main(path: Path, file: DecryptedSave, _: List[str]):
    game = GameSaveEditor(file)
    print(f"Healing player {game.player.names.first_name}")
    stats = game.player.stats.current
    game.player.healable.hp = stats.hp
    game.player.healable.mp = stats.mp
    file.hash_update()
    file.encrypt().save(path)
