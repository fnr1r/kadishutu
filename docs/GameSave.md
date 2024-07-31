# GameSave

Size: 449680 bytes (end at 0x6dc90)

## Decryption

The decryption algorithm is stored in [encryption.py](../src/kadishutu/encryption.py).

Credits to zmbkilla's SMTVV Save Editor for the algorithm and key.

```python
KEY = bytes([0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
             0x38, 0x39, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66,
             0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
             0x38, 0x39, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66])
```

## Structure

- 0x0 - 0x20 - SHA1 Hash of the rest of the file  
  (20 bytes)
- 0x4d8 - ????? - [First Name](#name-info)
- 0x4f0 - 0x500 - Time of Saving (UNKNOWN FORMAT)  
  (16 bytes)
- 0x529 - 0x52a - [DLC Flags](#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x5d0 - 0x5d4 - Play Time (in seconds)  
  (I'm guessing it's an unsigned int / u32 (4 bytes))
- 0x618 - 0x61a - Player [level](#level-info)?  
  (maybe... not really... maybe it's a gui thing)  
  (2 byte)
- 0x9d0 - ????? - [First Name... again](#name-info)
- 0x988 - 0x9b8 - Player [stats block](#stat-block)  
  (48 bytes)
- 0x9bc - 0x9c0 - Player [healable stats](#healable-stats)  
  (4 bytes)
- 0x9c8 - 0x9c9 - Player [level](#level-info)  
  (2 byte)
- 0x9e8 - ????? - [Last Name](#name-info)
- 0x9fc - ????? - [First Name](#name-info)
- 0xa10 - [Combined first and last name](#name-info)
- 0xa38 - 0xa78 - Player [skills](#skill-block)  
  (64 bytes)
- 0xa98 - 0xaa8 - Player [affinities](#affinity-block)  
  (16 bytes)
- 0xb38 - 0xb50 - Player [potentials](#potential-block)  
  (24 bytes)
- 0xb60 - ????? - [Demon table](#demon-info)
- 0x3d32 - 0x3d36 - Macca  
  (an unsigned int / u32 (4 bytes))
- 0x3d4a - 0x3d4e - Glory  
  (an unsigned int / u32 (4 bytes))
- 0x3d2e - ?????? - Summoned Demons (TODO)  
  (with indices of the demon table; from first to last)  
  (3 unsigned chars / u8s (3 bytes))
- 0x3d45 - ?????? - Player placement  
  (which slot the player is in, from 0 to 2; other values break it)  
  (an unsigned char / u8 (1 byte))
- 0x3ece - 0x3ed0 - Magatsuhi Gauge  
  (from 0% - 100% value)  
  (an unsigned short (2 bytes))
- 0x4c72 - ?????? - [Item Table](#item-table)
- 0x5129 - ?????? - [Essence Metadata Table](#essence-info)
- 0x568e - ?????? - [Coordinates](#coordinate-info)
- 0x7dc0 - 0x7de0 - Demon haunt data
- 0x1375e - ??????? - [Tracking](#tracking-info)
- 0x69a90 - ??????? - Settings????
- 0x69a91 - ??????? - Mitama Settings????  
  (an unsigned char / u8 (1 byte))
- 0x6a07f - ??????? - DLC Flags
  (0 when no dlc, 0x18 when all dlcs)
  (an unsigned char / u8 (1 byte))

<!--
a("difficulty", 0x54c, "H"),
# NOTE: Always 4????
a("stats_mystery_stuff", 0x9b8, "<l"),
a("player_stats2", 0x9c0, "II", "LV EXP"),
-->

## DLC info

It's an unsigned char / u8 (1 byte).

```txt
0x00000000
  01234567
```

- 0x01 - bit 0 - Not assigned to any DLC
  (leftovers of the Japanese Voice Pack DLC?)  
  (it does nothing when changed, but the game doesn't get rid of it)
- 0x02 - bit 1 - DLC 1 - Safety Difficulty
- 0x04 - bit 2 - DLC 2 - Mitama Dance of Wealth
- 0x08 - bit 3 - DLC 3 - Mitama Dance of EXP
- 0x10 - bit 4 - DLC 4 - Mitama Dance of Glory
- 0x20 - bit 5 - DLC 5 - Holy Will and Profane Dissent
- 0x40 - bit 6 - DLC 6 - Sakura Cinders of the East
- 0x80 - bit 7 - DLC 7 - 2 Sacred Treasures Set

NOTE: This value also appears in `SysSave`, but when starting the game, it will
be updated this value based on the DLCs installed, so changing it is pointless.

## Name info

WARNING: Name editing is currently broken. If you don't preserve the length of
the name, it will break in unexpected ways.

The max name length is 8 UTF-16 chars (16 bytes).

NOTE: It might not actually be UTF-16, because the Persona series and some
previous games use the JIS encoding.

The first name appears in 3 places in the file.
The last name - only once.

Then there's also a combined copy of both, separated by a space.

This is a massive TODO.

## Stats info

### Singular Stat value

A singular stat is represented by an unsigned short / u16 (2 bytes).

### Stat value set

A stat value set contains data in the following order:

- HP - Health (Health Points)
- MP - Mana (Magic Points)
- ST - Strength
- VI - Vitality
- MA - Magic
- AG - Agility
- LU - Luck
- (seemingly always) A NULL value

It's 16 bytes in total.

### Stat block

Stat blocks contain:

- Initial stats (stats that the demon should have at the current level)
- Stat changes (this includes changes from using Balms/Incenses, talking at the demon haunt (except for Aogami/Tsukuyomi))
- Current stats (stats that are actually used for calculations/displaying)

It's 48 bytes in total.

### Healable Stats

There are also healable stat blocks which (afaik) contain only:

- Current HP
- Current MP

Both of these can exceed the maximum from the current stat block.

## Level info

The level is stored as an unsigned short / u16 (2 bytes).

In-game it's initially capped at 99, except for... well... spoilers...

The value can exceed the maximum.

NOTE: Changing this value does not change the data in the initial stat block. This means you'll loose the stat points you'd gain at this level.

I recommend not changing this. EVER. Just use Gospels/Grimores.

## Skill info

### Singular Skill value

A skill value consists of:

- A mysterious  value
  (an unsigned int / u32 (4 bytes))
  (might be weather the skill can be learned)
- A skill ID
  (an unsigned int / u32 (4 bytes))

It's 8 bytes in total.

### Skill block

A skill block is an array of 8 singular skill values.

It's 64 bytes in total.

## Affinity info

NOTE: This might not matter, since editing this does not affect the actual affinities of the Demon.

### Singular Affinity value

A singular affinity is represented by an unsigned short / i16 (2 bytes).

Here are the possible values:

- 0 - Null
- 50 - Resist
- 100 - Neutral
- 125 - Weak
- 999 - Repel
- 1000 - Drain

### Affinity block

An affinity block is an array containing 7 values in the following order:

- Physical
- Fire
- Ice
- Electric
- Force
- Light
- Dark
- (there might be an 8th value as padding)

It's 14 or 16 bytes in total.

## Potential info

### Singular Potential value

A singular affinity is represented by a signed short / i16 (2 bytes).

In regular gameplay it ranges from -9 to 9.

### Potential block

An affinity block is an array containing 11 values in the following order:

- Physical
- Fire
- Ice
- Electric
- Force
- Light
- Dark
- Almighty
- Ailment
- Support
- Healing
- (maybe padding) an unknown value (usually a copy of previous ones)

It's 22 or 24 bytes in total.

## Demon info

### Demon ID

The demon ID is represented by an unsigned short / i16 (2 bytes).

0xffff is used to signal that the slot is free.

### Innate Skill ID

A singular affinity is represented by an unsigned short / i16 (2 bytes).

The ID of the innate skill.

Surprisingly, it's mutable and unlike changing affinities, it works.

NOTE: The player (most likely) also has a stored innate skill id, but I don't know where it's stored.

### Demon entry

Each demon entry is 0x1a8 (424 decimal) in size.

Here's the structure:

- 0x0 - 0x30 - [Stats block](#stat-block)
- 0x44 - 0x48 - Friendship
  (changes every time the demon is given the lower-grade gift)
  (an unsigned int / u32 (4 bytes))
- 0x48 - 0x4a - maybe_is_summoned
  (an unsigned short / u16 (2 bytes))
- 0x4a - 0x4c - dh_talks
  (something related to the demon haunt)
  (an unsigned short / u16 (2 bytes))
- 0x64 - 0x68 - [Healable stats](#healable-stats)  
  (4 bytes)
- 0x68 - 0x70 - Experience
  (an unsigned long long / u64 (8 bytes))
- 0x70 - 0x72 - [Level](#level-info)  
  (2 bytes)
- 0x72 - 0x74 - [Demon ID](#demon-id)  
  (2 bytes)
- 0x78 - 0xb8 - [Skills](#skill-block)  
  (64 bytes)
- 0xd8 - 0xe8 - [Affinities](#affinity-block)  
  (16 bytes)
- 0x180 - 0x198 - [Potentials](#potential-block)  
  (24 bytes)
- 0x198 - 0x200 - Innate skill  
  (2 bytes)

<!--
add_dat("x_magic_number", 64, "<l")
add_dat("statsx", 84, "<HH")
-->

### Demon table

The demon table start at 0xb60.

It contains AN amount of [demon entries](#demon-entry).

How much?

It's at least 24 (due to the in-game limit of 24 demons).

It might be +4/5 due to the fact that it has to store guests.  
(Yoko, Tao, Yuzuru, Ichiro and Demi-fiend)
(although Demi-fiend is not available until the end of the game)

A random diff between a DLC save file and that same save file after installing DLCs and saving gave me a result of 30.
(some random value changed for every demon in the demon table)

(A way to test this would be TPing to the Hall of Chaos and battling the
Demi-fiend at a point where you have all 4 other party members. TODO, since I
haven't fully figured out the coordinate and map system)

Table end offsets per table size:

- 24 - 0x3320
- 30 - 0x3d10

## Item info

### Item amount

The amount of an item is stored an unsigned char / u8 (1 byte).

This can exceed the in-game item limit.

### Item Table

It's a massive array of item amounts.

The table starts at 0x4c72 with consumable items and ends at 0x4d4f.

Then there's relics from 0x4ed0 to 0x4f01.  
Then there's essences from 0x4da9 to 0x4ebc.  
Then there's key items from 0x4f02 to 0x4fca.  
Then there's relics (again) from 0x4fca to 0x4f11.

NOTE: Essences can only ever have a value of 1.

## Essence info

It's an array of fields, each one correlates to an item field asociated with an essence.

In a way essences are both items, and not.

The formula for it is: `absoulute_item_offset + 0x380`  
where the item is an essence.

Here are possible values for each field:

- 0 - Not owned  
  (default)
- 2 - New  
  (after getting an essence from a box)
- 4 - ???? (possible)  
  (achieved when giving an essence without changing this value)
- 6 - Owned  
  (after highliting it in the menu)
- 16 - Used  
  (after fusion)

## Coordinate info

Coordinates are stored in 0x568e.

Positional coordinates are stored as a signed int / i32 (4 bytes).  
Rotational coordinates are stored as an unsigned int / u32 (4 bytes).

<!--
TODO: Figure this shit out
(It's too close for comfort, oh)
-->

## Tracking info

Tracking is done within an unsigned char / u8 (1 byte).
(or maybe an unsigned short / u16 (2 bytes))

The game track the following actions:

- 0x1375e - Giving boxes to demons
- 0x180f? - Using essences

The following things are not tracked:

- Using Balms and Incenses
