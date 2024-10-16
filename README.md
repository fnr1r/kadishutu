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

(fun fact, this project also works on Windows 7 (the best version) with VxKex
and Python 3.9)

### Additional setup

Some data is not bundled with the editor. While not strictly necesary, adding
it gives you a better experience with the editor.

The files can be dumped/saved/exported with
[umodel](https://www.gildor.org/en/projects/umodel).

(don't use the Linux version, it's outdated)

[Fmodel](https://fmodel.app/) should also work, but it's kinda hit or miss for
me.

#### Game data

```txt
Game/Blueprints/Gamedata/BinTable/GodParameter/Table/GodParameterDataTable.uexp
```

(GodParameter means Miracle)

#### Game image data

```txt
Game/Design/UI/CharaIcon/Textures/*
Game/Design/UI/Icon/Element/Textures/icon_element_01.tga
Game/Design/UI/LoadingCharaIcon/*
```

#### App data directory

For Linux, it's usually:

`$HOME/.local/share/kadishutu`

For Windows, it's:

`$HOME/AppData/Local/kadishutu`

And for macOS, it's:

`$HOME/Library/Application Support/kadishutu`

The app can also be made portable by setting the `PORTABLE_APP` environment
variable. Then data is stored in/loaded from:

`./_appdata/data`

(more info in [paths.py](src/kadishutu/paths.py))

## Usage

### GUI

You can open the GUI by running `kadishutu gui $OPTIONALLY_A_SAVE_FILE` in a
terminal or by double-clicking the executable.

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
from kadishutu import DecryptedSave, GameSaveEditor
from pathlib import Path

path = Path(...)
savefile = EncryptedSave.open(path).decrypt()
game = SaveEditor(savefile)

stats = game.player.stats
stats.max_with_sbis()
stats.current.hp = 999
stats.current.mp = 999

# Yes. This surprisingly works.
stats.current.strength = 0xffff

game.player.healable.hp = 999
game.player.healable.mp = 999
game.macca = 9999999
game.items.from_name("Big Glory Crystal").amount = 99

savefile.hash_update()
savefile.encrypt().save(path)
```

## What works?

NOTE: This is tested with the Switch version of the game (`010069C01AB82000`
with all DLCs more specifically), but it also works with the PC version.

- Encryption/Decryption
- Viewing and editing of the following values
  - Player Names
  - Time of saving (it's a bit weird, but it works)
  - Used DLCs (this will not give you DLC-exclusive content)  
    (it's mainly for importing a save file from a copy with DLCs)
  - Play Time
  - Miracle (and unlocking them)
  - Summoned demons and player placement
  - For the player and demons
    - Affinities, Potentials, Stats, Skills, Exp, Lvl, Innate Skill
  - Player stat points
  - Demons (i.e. Demon IDs)
  - Team composition (summoned demons and their order)
  - Macca, Glory
  - Miracles (+unlocking most of them)
  - Items
  - Essences (kinda)
  - Position
  - Early compendium and quest support
  - Alignment
  - Number of cycles and endings
- Summoning new Demons kinda works, but it's not recommended, because the demon
  block is not fully understood
- SysSave is documented, but not implemented

## What doesn't?

- The cli is utter garbage
- This needs a solid rework

## What's planned?

- Editing more data
  - Properly implementing compendium and quest support  
    (Tao and Yoko might be in a separate block)
  - Full demon support
- Better CLI
- Allowing the user to add files that modify the demon/skill database, in
  corelation with mods
- Rewrite the core in Rust (once the format is better understood)

## Documentation

The documentation for the save files is in the docs folder:

[GameSave.md](docs/GameSave.md)
[SysSave.md](docs/SysSave.md)

And [here's](docs/Troubleshooting.md) the troubleshooting info.

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
