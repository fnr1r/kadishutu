# Qadištu (カディシュトゥ, Kadishutu) save editor

A save editor for Shin Megami Tensei V: Vengeance.

## Installation

I recommend installing this with pipx.

```shell
pipx install git+https://github.com/fnr1r/kadishutu.git
```

Regular pip might also work, but it also might not due to
[PEP 668](https://peps.python.org/pep-0668/). It's also more of a hastle.
Pipx is built for installing Python apps and handles updates better.

In other words, if you want to update, run:

```shell
pipx upgrade kadishutu
```

[Here's](https://pipx.pypa.io/latest/) more info on pipx.

[Binaries](https://github.com/fnr1r/kadishutu/releases) are also available,
but because they're built with pyinstaller, they might get flagged by your
antivirus.

## Usage

### GUI

You can open the GUI by running `kadishutu gui $OPTIONALLY_A_SAVE_FILE` in a
terminal.

### In a terminal

Available subcommands:

- `decrypt`
- `edit`
- `encrypt`
- `help`
- `inspect`
- `run_script`
- `update_hash`

#### Edit subcommand

##### DLC

- clear - Clears all DLC flags
- print - Prints what DLCs were used
- remove - Removes a DLC flag

### As a library

```python
from pathlib import Path
from kadishutu.file_handling import EncryptedSave
from kadishutu.game import SaveEditor

path = Path(...)
savefile = EncryptedSave.open(path).decrypt()
game = SaveEditor(savefile)

stats = game.player.stats
stats.max_with_sbis()
stats.current.hp = 999
stats.current.mp = 999
game.player.healable.hp = 999
game.player.healable.mp = 999
game.macca = 9999999
game.items.from_name("Big Glory Crystal").amount = 99

savefile.hash_update()
savefile.encrypt().save(path)
```

## What works?

NOTE: This is tested with the Switch version of the game (`010069C01AB82000`
with all DLCs more specifically). It might work with the PC version.

- Encryption/Decryption
- Viewing and editing of the following values
  - Used DLCs (this will not give you DLC-exclusive content)  
    (it's mainly for importing a save file from a copy with DLCs)
  - Macca, Glory
  - Summoned demons and player placement
  - For the player and demons
    - Affinities, Potentials, Stats, Skills, Exp, Lvl (only for demons)
  - Only for demons:
    - Demon ID, Innate Skill
  - (some) Items (I need the item table for this game)
  - Essences (kinda) (it's experimental)
- Viewing some information (without editing):
  - Play Time (but not time of saving, it's in a weird format)
  - Player Name
- Manual editing after decryption

## What doesn't?

- Play time is in a weird format
- The cli is utter garbage
- This needs a solid rework
- Name changing is broken (for names of different length)
- Changing affinities is also broken

## What's planned?

- Better CLI
- GUI
- Changing your alignment
- Allowing the user to add files that modify the demon/skill database, in
  corelation with mods

## Documentation

The documentation for the save files is in the docs folder:

[GameSave.md](docs/GameSave.md)
[SysSave.md](docs/SysSave.md)

## Credits

- [zmbkilla's SMTVV Save Editor](https://github.com/zmbkilla/SMTV-VSaveEditor/tree/e8def6cd038d1a3d23d5bdc7612b1fd13808dfaf)
  for most working offsets, AES key, Innate Skill IDs, Demon IDs

And some save editors for the OG version:

- [Aogami Save Editor](https://github.com/supremetakoyaki/Aogami)
  for the inspiration for the name
- this save editor
  (<https://github.com/Amuyea-gbatemp/Shin-Megami-Tensei-V-Save-Editor>)
  for info on how other types of data are stored

## External links

[![This project is also on GameBanana.]("https://gamebanana.com/tools/embeddables/17599?type=large")](https://gamebanana.com/tools/17599)
