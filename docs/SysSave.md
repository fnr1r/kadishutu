# GameSave

## Decryption

Same as for game saves. Chech out [GameSave.md](GameSave.md#decryption) for more info.

## Structure

- 0x0 - 0x20 - SHA1 Hash of the rest of the file  
  (20 bytes)
- 0x608 - 0x609 - Mitama Dance of Glory
  (a padded bool (1 byte))
- 0x609 - 0x60a - Mitama Dance of Wealth
  (a padded bool (1 byte))
- 0x60a - 0x60b - Mitama Dance of EXP
  (a padded bool (1 byte))
- 0x60b - 060c - Game-wide [DLC info](#dlc-info)
  (an unsigned char / u8 (1 byte))
- 0x124c - 0x124d - Game-wide [DLC info](#dlc-info)
  (an unsigned char / u8 (1 byte))

## DLC info

It's an unsigned char / u8 (1 byte).

```txt
0x00000000
  8  -> 1
```

- 0x01 - bit 7 - Not assigned to any DLC
- 0x02 - bit 6 - DLC 1 - Safety DLC
- 0x04 - bit 5 - DLC 2 - Mitama Dance of Wealth
- 0x08 - bit 4 - DLC 3 - Mitama Dance of EXP
- 0x10 - bit 3 - DLC 4 - Mitama Dance of Glory
- 0x20 - bit 2 - DLC 5 - Holy Will and Profane Dissent
- 0x40 - bit 1 - DLC 6 - Sakura Cinders of the East
- 0x80 - bit 0 - DLC 7 - 2 Sacred Treasures Set

NOTE: The game will update this value, so changing it is pointless.
