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

- 0x0 - 0x14 - SHA1 Hash of the rest of the file  
  (20 bytes)
- 0x28 - 0x2c - [Difficulty-related?](#difficulty-values)
  (an unsigned int / u32 (4 bytes))
- 0x4d8 - 0x4e8 - [Save name](#name-info)
- 0x4f0 - 0x4f4 - [???](#time-of-saving-info)  
  (4 bytes)
- 0x4f4 - 0x4fc - [Time of Saving](#time-of-saving-info)  
  (an unsigned long long / u64 (8 bytes))
- 0x4fc - 0x4fd - [Difficulty](#difficulty-values)
- 0x4fd - 0x4fe - ????
- 0x4fe - 0x500 - ????
- 0x500 - 0x502 - ????
- 0x502 - 0x503 - [Cycles](#cycles-value)  
  (an unsigned char / u8 (1 byte))
- 0x503 - 0x504 - [Endings](#endings-value)  
  (an unsigned char / u8 (1 byte))
- 0x504 - 0x524 - [Demon Icons Block](#demon-icons-block)  
  (32 bytes)
- 0x524 - 0x528 - [Save location](#save-location)  
  (an unsigned int / u32 (4 bytes))
- 0x528 - 0x529 - Clear flag  
  (a padded bool (1 byte))
- 0x529 - 0x52a - [DLC Flags](#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x5d0 - 0x5d4 - Play Time (in seconds)  
  (I'm guessing it's an unsigned int / u32 (4 bytes))
- 0x5d4 - 0x5d5 - Moon phase
- 0x618 - 0x61a - Player [level](#level-info)?  
  (maybe... not really... maybe it's a gui thing)  
  (an unsigned short / u16 (2 bytes))
- 0x988 - 0x9b8 - Player [stats block](#stat-block)  
  (48 bytes)
- 0x9bc - 0x9c0 - Player [healable stats](#healable-stats)  
  (4 bytes)
- 0x9c0 - 0x9c8 - Player Experience  
  (an unsigned long long / u64 (8 bytes))
- 0x9c8 - 0x9ca - Player [level](#level-info)  
  (an unsigned short / u16 (2 bytes))
- 0x9d0 - 0x9e0 - [First name](#name-info)
- 0x9e8 - 0x9f8 - [Last name](#name-info)
- 0x9fc - 0xa0c - [First name again](#name-info)
- 0xa10 - 0xa38 - [Combined name](#name-info)
- 0xa38 - 0xa78 - Player [skills](#skill-block)  
  (64 bytes)
- 0xa98 - 0xae0 - Player [affinities](#affinity-block)  
  (112 bytes)
- 0xb38 - 0xb50 - Player [potentials](#potential-block)  
  (24 bytes)
- 0xb50 - 0xb52 - Player [innate skill](#innate-skill-id)  
  (an unsigned short / u16 (2 bytes))
- 0xb60 - 0x3d10 - [Demon table](#demon-info)
- 0x3d10 - 0x3d2e - Party menu demon order  
  (with indices of the demon table; from first to last)  
  (30 unsigned chars / u8s (30 bytes))
- 0x3d2e - 0x3d31 - Summoned Demons (TODO)  
  (with indices of the demon table; from first to last)  
  (3 unsigned chars / u8s (3 bytes))
- 0x3d31 - 0x3d32 - Max Demon Stock  
  (an unsigned char / u8 (1 byte))
- 0x3d32 - 0x3d36 - Macca  
  (an unsigned int / u32 (4 bytes))
- 0x3d45 - 0x3d46 - Player placement  
  (which slot the player is in, from 0 to 2; other values break it)  
  (an unsigned char / u8 (1 byte))
- 0x3d4a - 0x3d4e - Glory  
  (an unsigned int / u32 (4 bytes))
- 0x3d4e - 0x3de0 - [Miracle Block](#miracle-info)
- 0x3ece - 0x3ed0 - Magatsuhi Gauge  
  (from 0% - 100% value)  
  (an unsigned short / u16 (2 bytes))
- 0x49d8 - 0x4c20 - Demon data???
- 0x4c5a - 0x4c5c - Yoko + Tao registered???
- 0x4c72 - 0x4f11 - [Item Table](#item-table)
- 0x5129 - 0x523c - [Essence Metadata Table](#essence-info)
- 0x567e - 0x5682 - [Map ID 1](#map-ids)  
  (an unsigned int / u32 (4 bytes))
- 0x5682 - 0x5686 - [Map ID 2](#map-ids)  
  (an unsigned int / u32 (4 bytes))
- 0x568e - 0x569a - [Coordinates](#coordinate-info)  
  (3 floats / f32 (12 bytes))
- 0x56a6 - 0x56ae - [Rotation](#coordinate-info)  
  (2 floats / f32 (8 bytes))
- 0x67a3 - 0x67f6 - [Miracle unlock data](#miracle-unlocks)
- 0x68c5 - 0x68c6 - [Last used layline fount ID](#layline-fount-info)  
  (an unsigned char / u8 (1 byte))
- 0x72ca - 0x72cb - ????
- 0x7dc0 - 0x7de0 - Demon haunt data
- 0x80a2 - 0x80d2 (?) - Layline unlock data
- 0x1375e - ??????? - [Tracking](#tracking-info)
- 0x18282 - 0x2db42 - [Demon Compendium](#demon-compendium)
- 0x5a760 - 0x5b0a0 - Quest data????
- 0x69a82 - 0x69a?? - [NEW](#new-flag-info)
- 0x69a90 - ??????? - Settings????
- 0x69a91 - ??????? - Mitama Settings????  
  (an unsigned char / u8 (1 byte))
- 0x69ca4 - 0x69ca4 - Story progress data?
- 0x69cf7 - 0x69cf8 - [Alignment (Vengeance)](#canon-of-vengeance)
- 0x6a07f - ??????? - DLC Flags
  (0 when no dlc, 0x18 when all dlcs)
  (an unsigned char / u8 (1 byte))
- 0x6a08a - 0x6a08b - [Cycles](#cycles-value)  
  (an unsigned char / u8 (1 byte))
- 0x6a08b - 0x6a08c - [Endings](#endings-value)  
  (an unsigned char / u8 (1 byte))
- 0x6a08d - 0x6a08e - NewGame+ Flag???  
  (a padded bool (1 byte))

<!--
a("difficulty", 0x54c, "H"),
# NOTE: Always 4????
a("stats_mystery_stuff", 0x9b8, "<l"),
a("player_stats2", 0x9c0, "II", "LV EXP"),
-->

## Note about save screen data

Save screen data is loaded once when starting the game, which (reasonably)
assumes the files won't be modified while it's running.

When loading a modified save file and saving over it, the save screen data is
synced with what's in the file.

This includes (but is not limited to):

- [Save screen name](#name-info)
- [Time of saving](#time-of-saving-info)
- [DLC info](#dlc-info)
- Play time
- Summoned demons and protagonist placement

This is also why the workaround from
[issue #1](https://github.com/fnr1r/kadishutu/issues/1#issuecomment-2255997834)
worked.

### Cycles value

It's an unsigned char / u8 (1 byte) with an in-game cap of 99.

### Endings value

- 0x01 - Creation - Neutral
- 0x02 - Creation - Law
- 0x04 - Creation - Chaos
- 0x08 - Creation - True Neutral
- 0x10 - Vengeance - Law
- 0x20 - Vengeance - Chaos

## Difficulty values

For some reason, there are two values that dictate difficulty.

Data for 0x20:

- Clear save from Bai Gaming: 1371 c242
- Hard: ac4b 2f81
- Normal: 0000 0000
- Casual: 1600 0000
- Safety: 1600 0000

Data for 0x4fc (the real difficulty???):

- Clear save from Bai Gaming: 82????
- Hard: 03
- Normal: 02
- Casual: 01
- Safety: 00

Godborn IS NOT a difficulty setting, so it's (most likely) stored
somewhere else.

## Name info

The max name length is 8 UTF-16 chars (16 bytes).

The game does let you get away with a longer name if you don't overwrite
other important data.

- 0x4d8 - First name (Save screen)  
  (std 8 UTF-16 chars (16 bytes))  
  (max 12 UTF-16 chars (24 bytes))
- 0x9d0 - First name (Menus, Dialogue)  
  (std 8 UTF-16 chars (16 bytes))  
  (max 12 UTF-16 chars (24 bytes))
- 0x9e8 - Last name (Dialogue)  
  (std 8 UTF-16 chars (16 bytes))  
  (max 10 UTF-16 chars (24 bytes))
- 0x9fc - First name (Also dialogue)  
  (std 8 UTF-16 chars (16 bytes))  
  (max 10 UTF-16 chars (24 bytes))
- 0xa10 - First and last name (Stat screen)  
  (std 17 UTF-16 chars (34 bytes))  
  (max 20 UTF-16 chars (40 bytes))

NOTE: Name at 0x4d8 gets overwritten by 0x9d0 every time you save.

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

## Time of saving info

The datetime is at 0x4f4 (an unsigned long long / u64 (8 bytes)).

An excerpt from Unreal Engine 4's source code, since
[it's not available to everyone](https://www.youtube.com/watch?v=NCvnLFF7IYM).

```cxx
/**
 * Implements a date and time.
 *
 * Values of this type represent dates and times between Midnight 00:00:00, January 1, 0001 and
 * Midnight 23:59:59.9999999, December 31, 9999 in the Gregorian calendar. Internally, the time
 * values are stored in ticks of 0.1 microseconds (= 100 nanoseconds) since January 1, 0001.
 *
 * To retrieve the current local date and time, use the FDateTime.Now() method. To retrieve the
 * current UTC time, use the FDateTime.UtcNow() method instead.
 *
 * This class also provides methods to convert dates and times from and to string representations,
 * calculate the number of days in a given month and year, check for leap years and determine the
 * time of day, day of week and month of year of a given date and time.
 *
 * The companion struct FTimespan is provided for enabling date and time based arithmetic, such as
 * calculating the difference between two dates or adding a certain amount of time to a given date.
 *
 * Ranges of dates and times can be represented by the FDateRange class.
 *
 * @see FDateRange
 * @see FTimespan
 */
struct FDateTime
{
  // Truncated
private:

  /** Holds the ticks in 100 nanoseconds resolution since January 1, 0001 A.D. */
  int64 Ticks;
};
```

[File URL](https://github.com/EpicGames/UnrealEngine/blob/4.27.2-release/Engine/Source/Runtime/Core/Public/Misc/DateTime.h)

File path: `/Engine/Source/Runtime/Core/Public/Misc/DateTime.h`

0x4fc is some 4 byte value that affects the time.

## Demon icons block

### Demon icon item

- Demon ID (an unsigned int / u32)  
  u32::MAX_INT if none  
  0x0172 if OG Nahobino
- Demon Level (an unsigned int / u32)  
  0 if none

### Demon icon list

4 demon icon items.

## Save location

(an unsigned int / u32 (4 bytes))

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

NOTE: For demons, if the current stats are different from the sum of initial
stats and changes, then at some point the game will reset them. This does not
apply for the player (for some reason).

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

An affinity block is an array containing many values in the following order:

- Copies of elemental values
- Ailments
- Physical
- Fire
- Ice
- Electric
- Force
- Light
- Dark

NOTE 2: When using an essence to inherit affinities as Nahobino, your
potentials also get updated based on your miracles.

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
  (48 bytes)
- 0x44 - 0x48 - Friendship  
  (changes every time the demon is given the lower-grade gift)  
  (an unsigned int / u32 (4 bytes))
- 0x48 - 0x4a - maybe_is_summoned  
  (an unsigned short / u16 (2 bytes))
- 0x4a - 0x4c - dh_talks  
  (something related to the demon haunt)  
  (an unsigned short / u16 (2 bytes))
- 0x58 - 0x5c - old_is_summoned  
  (an unsigned int / u32 (4 bytes))
- 0x60 - 0x61 - is_summoned
  (0x00 for not summoned, 0x06 for summoned)
- 0x64 - 0x68 - [Healable stats](#healable-stats)  
  (an unsigned int / u32 (4 bytes))
- 0x68 - 0x70 - Experience  
  (an unsigned long long / u64 (8 bytes))
- 0x70 - 0x72 - [Level](#level-info)  
  (an unsigned short / u16 (2 bytes))
- 0x72 - 0x74 - [Demon ID](#demon-id)  
  (an unsigned short / u16 (2 bytes))
- 0x78 - 0xb8 - [Skills](#skill-block)  
  (64 bytes)
- 0xd8 - 0xe8 - [Affinities](#affinity-block)  
  (16 bytes)
- 0x108 - 0x148 - [Affinities](#affinity-block)  
  (64 bytes)
- 0x148 - 0x14a - something (0xfeff)
- 0x150 - 0x151 - something (0x01)
- 0x154 - 0x156 - something (0xffff)
- 0x158 - 0x160 - something (0x0100 times 4)
- 0x160 - 0x162 - something (fight counter)
- 0x180 - 0x198 - [Potentials](#potential-block)  
  (24 bytes)
- 0x198 - 0x19c - [Innate skill](#innate-skill-id)  
  (an unsigned int / u32 (4 bytes))
- 0x19c - 0x19d - something (0x01)

<!--
add_dat("x_magic_number", 64, "<l")
add_dat("statsx", 84, "<HH")
-->

### Empty demon entry

0x1a8 sized array with nulls except for:

- 0x72 - 0x74 - Demon ID - 0xffff
- 0x74 - 0x76 - ???????? - 0x0001
- 0x110 - 0x148 - Affinities - repeated 0x6400

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

## Miracle info

### Miracle enum

It's an unsigned char / u8 (1 byte).

```txt
0x00000000
  01234567
```

- 0x01 - bit 0 - Bought
- 0x02 - bit 1 - Seen
- 0x04 - bit 2 - Enabled

Based on:

- 00 - NONE
- 02 - Seen
- 07 - Learned
- 03 - Shows up sometimes
- 01, 04, 05, 06 - NEVER APPEARS

NOTE: This might be a bitflag.

### Miracle block

An array of miracle values of unknown size.

- 0x67a3 - bit 1 - First one

### Miracle unlocks

It's packed bools.

Da'at: Minato???: 0x67a3 - 0x67a9  
Da'at: Shinagawa???: 0x67b7 - 0x67bc  
Da'at: Shinjuku???: 0x67df - 0x67e5  
Da'at: Taito???: 0x67e8 - 0x67ef  
Special: 0x67f3 - 0x67f6

Supremacy, Doctrine, Awakening, Cosmos

- 0x67a3
  - Art of Essences I
  - Demon Proficiency I
  - Divine Proficiency I
  - Divine Garrison I
  - Recover
  - Support
- 0x67a4
  - Divine Amalgamation
  - Divine Garrison II
  - Light
  - Dark
  - Ailment
- 0x67f3
  - Inheritance Violation
- 0x67f4
  - Rank Violation
- 0x67f5
  - Moral Transcendence
    (NOTE: requires bit 4 of byte 0x69ce6 to be set to 1)

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

## Location info

### Map IDs

0x567e and 0x5680 store the current map info.

### Coordinate info

Positional coordinates are stored as a float / f32 (4 bytes).  

<!--
TODO: Figure this shit out
(It's too close for comfort, oh)
-->

### Layline fount info

ID of the last used layline.

Recommended for tests: 0x31 - Tokyo Diet Building  
(loads the fastest)

WARNING: IF THE LAST LAYLINE FOUNT IS INVAILD, YOU GET THROWN TO THE TITLE SCREEN.

## Tracking info

Tracking is done within an unsigned char / u8 (1 byte).
(or maybe an unsigned short / u16 (2 bytes))

The game track the following actions:

- 0x1375e - Giving boxes to demons
- 0x180f? - Using essences

The following things are not tracked:

- Using Balms and Incenses

## Demon Compendium

Array indexed by the demon ID.

Each entry has a size of 0xe0 consists of:

- 0x0 - 0x10 - [Stat block](#stat-value-set)
  (registers stat changes)  
  (16 bytes)
- 0x30 - 0x50 - Skill block
  (registers only skill IDs)  
  (32 bytes?)

Assuming Eisheth (ID 394) is the last registerable demon, the table ends at
0xdb42.

## NEW flag info

- 0x69a82 - Skills NEW flag  
  (bool)
- 0x69a83 - Items NEW flag  
  (bool)
- 0x69a85 - Party NEW flag  
  (bool)
- 0x69a8e - bit 1 - Dashing popup?
- 0x69a8e - bit 3 - Magatsuhi crystal popup?
- 0x69a8e - bit 5 - Jumping popup?
- 0x69a8e - bit 7 - Climbing points popup?
- 0x69a90 - bit 3 - Treasure boxes popup?
- 0x69a90 - bit 1 - Quest info popup?
- 0x69a8f - bit 1 - Battle info popup?

- 0x69ca2 - Student talk data

## Alignment info

### Canon of Vengeance

Data about alignment values is in a different doc (for now).

[Here's a copy.](cheatroom_blog_post_translation.md)

## Notes

There must be a bit which changes the name from Netherworld to Da'at.

0x69c87 - 0x69c88 seems to be a turn counter?

0x69c88 seems to contain beaten bosses.

Changing 0x69cdc affects the layline menu, removing options.

Changing 0x69cdd from 0x60 back to 0x6b removed button prompts from the
bottom-left hand corner of the screen.

Changing 0x69ced affects the X menu.

Changing 0x69cef from 0x10 back to 0x00 makes the game grant the player the dlc
items again.

Save locations:

- 0x01 - Empyrean
- 0x05 - Terminal Room
- 0x07 - Temple of Eternity 1F
- 0x21 - Tamachi
- 0x22 - Mita
- 0x23 - Shiba
- 0x41 - North Shinagawa
- 0x44 - Ginza
- 0x46 - Sukiyabashi
- 0x48 - Nihonbashi
- 0x4c - Awajicho
- 0x4d - Akihabara
- 0x4f - Mansei Bridge
- 0x50 - Akihabara Electric Town
- 0x52 - Ochanomizu
- 0x53 - Kanda-no-yashiro
- 0x55 - Otemachi
- 0x57 - Tokyo Station
- 0x59 - Ueno
- 0x5a - Ueno Park
- 0x5b - Shinobazu Pond
- 0x5f - Asakusa
- 0x61 - Komagata
- 0x64 - Umayabashi
- 0x6e - Jouin High School Gates
- 0x74 - Asakusa Main Street
- 0x75 - Hall of Chaos
- 0x79 - Empyrean Throne Room
- 0x8b - Shakan: 4th Stratum

Maria alignment test data:

```txt
Save location: 0x01
{
    "id": "0x2",
    "name": "Empyrean - Maria",
    "map_upper": "0x00000010",
    "map_lower": "0x00000000",
    "coordinates": "52ec6d450f2e06c700302345",
    "rotation": "1b29343fc2df353f"
},
```

Analyze data regex: `\+0005[def][0-9a-f]{3}`

## Ignore list

- 0x7e28 - 0x7e2a
- 0x8162 - 0x8166
<!-- - 0x8d7a - 0x8d7c -->
- 0x8d70 - 0x8dd0
- 0x11df0
- 0x11e08
- 0x11e20
- 0x11e4c - 0x11e4e
- 0x11e70 - 0x11e71
