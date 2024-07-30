from kadishutu.file_handling import DecryptedSave
from kadishutu.game import SaveEditor
from pathlib import Path
from typing import List


def main(path: Path, file: DecryptedSave, _: List[str]):
    game = SaveEditor(file)
    stats = game.player.stats.current
    game.player.healable.hp = stats.hp
    game.player.healable.mp = stats.mp
    file.encrypt().save(path)
