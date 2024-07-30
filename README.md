# Qadištu (カディシュトゥ, Kadishutu) save editor

A save editor for Shin Megami Tensei V: Vengeance.

## Usage

I recommend installing this with pipx.
I might release an exe/app/elf version soon™.

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

### In a terminal

Available subcommands:

- `decrypt`
- `edit`
- `encrypt`
- `help`
- `inspect`
- `run_script`
- `update_hash`

### GUI

You can open the GUI by running `kadishutu gui $OPTIONALLY_A_SAVE_FILE`.

#### Edit subcommand

##### DLC

- clear - Clears all DLC flags
- print - Prints what DLCs were used
- remove - Removes a DLC flag

## What works?

NOTE: This is tested with the Switch version of the game (`010069C01AB82000`
with all DLCs more specifically). It might work with the PC version.

- Encryption/Decryption
- Printing select information about the (game) save file like:
  - Player Name
  - Macca, Glory, Play Time (but not time of saving, it's in a weird format)
  - Affinities, Skills, Stats, Exp, Lvl
  - (for demons) Innate Skills, IDs
  - (some) Items (I need the item table for this game)
- Manual editing after decryption, for example:
  - Skill replacement for demons
  - Name replacement (remember to replace the name in all places, or the game
    will not load the save file)

## What doesn't?

- The cli is utter garbage
- This needs a solid rework
- Name changing is broken (for names of different length)
- Changing affinities is also broken

## What's planned?

- Better CLI
- GUI
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
