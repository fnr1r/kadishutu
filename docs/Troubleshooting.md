# Troubleshooting

## "UnicodeDecodeError: '(name)' codec can't decode byte 0x(value) in position (offset): illegal multibyte sequence."

It's caused by Python thinking a UTF-8-encoded file (the default and used
everywhere in this repo) is in some different encoding.

### Solution 1: Upgrade

It's fixed in commit
[781ed59](https://github.com/fnr1r/kadishutu/commit/781ed593e018c7c65059633a3545bd414502cf89).

I tested it on Windows 7 and it should work.

### Solution 2: Change settings (Windows)

If it still happens (which is possible if it's caused by a different file).

Open the control panel, open "Region" from "Clock and Region", and open "Change system locale" from the "Administrative" tab.

Check the "Beta: Use Unicode UTF-8 with worldwide language support" checkbox at the bottom and restart your PC.

NOTE: This can also cause issues with other apps.

### Solution 3: Edit the data file

Find multibyte characters and replace them. For example:

- "š" with "s" (in "Qadištu")
- "é" with "e" (in "Souffle D'éclair")
- "∞" with "inf"

### Sources

[Solution 3 and some info for 2 - pewbeyeaj on GameBanana](https://gamebanana.com/posts/12025667)

[Solution 2 - diphyleia on GameBanana](https://gamebanana.com/posts/11873594)

## Changes made to resistances are reverted

This is expected (at least for demons) since those values are only copies.

## Changes made to skill potentials are reverted

If the skill potential of a demon is below 1, the skill potential can't be
increased (neither in-game with sutras, nor by editing).

As for the player, it might be recalculated based on bought miracles.
