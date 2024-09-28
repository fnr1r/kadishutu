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


import inquirer
from kadishutu import DecryptedSave, GameSaveEditor
from typing import Any, Dict, List, Tuple


ENDINGS = [
    "NEUTRAL", "LAW", "CHAOS", "SECRET",
]


def main(path: Path, file: DecryptedSave, _: List[str]):
    game = GameSaveEditor(file)

    print("Quick note: Carrying over demons is not supported. Sorry :(")
    print("Note 2: More carry-over options may be added in the future")
    questions = [
        inquirer.Checkbox(
            "endings",
            message="Select your endings",
            choices=ENDINGS
        ),
        inquirer.Confirm(
            "grant_endings",
            message="Mark those endings as achieved?",
        ),
    ]
    answers_maybe = inquirer.prompt(questions)
    assert answers_maybe is not None
    answers: Dict[str, Any] = answers_maybe
    endings: List[str] = answers["endings"]

    item_changes: List[Tuple[str, int]] = [
        ("Large Glory Crystal", 1),
        ("Medicine", 20),
        ("Chakra Drop", 5),
        ("Revival Bead", 5),
        ("Spyglass", 20),
        ("Smoke Ball", 5),
    ]
    essence_changes: List[int] = []
    if "NEUTRAL" in endings:
        # Nuwa
        essence_changes.extend([361, 435])
        item_changes.extend([
            ("Agility Balm", 10),
            ("Luck Balm", 10),
            ("Agility Incense", 10),
            ("Luck Incense", 10),
        ])
    if "LAW" in endings:
        # Abdiel
        essence_changes.extend([461, 477])
        item_changes.extend([
            ("Vitality Balm", 10),
            ("Vitality Incense", 10),
            ("Grimoire", 10),
            ("Gospel", 3),
            ("Whittled Goat", 1),
        ])
    if "CHAOS" in endings:
        essence_changes.extend([
            409, # Hayataro
        ])
        item_changes.extend([
            ("Strength Balm", 10),
            ("Magic Balm", 10),
            ("Strength Incense", 10),
            ("Magic Incense", 10),
        ])
    if "SECRET" in endings:
        essence_changes.extend([
            421, # Shiva
            311, # Khonsu
            335, # Fionn mac Cumhaill
        ])
        item_changes.extend([
            ("Health Balm", 4),
            ("Stamina Balm", 4),
            ("Health Incense", 4),
            ("Stamina Incense", 4),
        ])
    if all([
        ending in endings
        for ending in ENDINGS
    ]):
        item_changes.extend([
            (f"{i} Sutra", 10)
            for i in [
                "Battle", "Fire", "Ice", "Elec", "Force", "Light", "Dark",
                "Destruction", "Calamity",
            ]
        ] + [
            (f"{i} Sutra", 5)
            for i in ["Healing", "Aiding"]
        ])

    items = game.items
    for name, amount in item_changes:
        items.from_name(name).amount += amount

    essences = game.essences
    for no in essence_changes:
        essence = essences.from_id(no)
        essence.amount = 1
        essence.give()

    if answers["grant_endings"]:
        from kadishutu.core.game_save.game import Endings
        def grant_ending(ending: str):
            ending_val = Endings["Creation" + ending.lower().capitalize()]
            print(ending, ending_val)
            game.cycles += 1
            game.endings |= ending_val
            game.endings_copy |= ending_val
        for i in endings:
            grant_ending(i)
        game.cycles_copy = game.cycles

    file.hash_update()
    file.encrypt().save(path)
