# SysSave

## Decryption

Same as for game saves. Chech out [GameSave.md](GameSave.md#decryption) for more info.

## Structure

- 0x0 - 0x20 - SHA1 Hash of the rest of the file  
  (20 bytes)
- 0x5ff - 0x600 - Message speed  
  (0 - slow, 1 - normal, 2 - fast)  
  (an unsigned char / u8 (1 byte))
- 0x60a - 0x60c - ????
- 0x608 - 0x609 - Mitama Dance of Glory  
  (a padded bool (1 byte))
- 0x609 - 0x60a - Mitama Dance of Wealth  
  (a padded bool (1 byte))
- 0x60a - 0x60b - Mitama Dance of EXP  
  (a padded bool (1 byte))
- 0x60b - 060c - Game-wide [DLC info](GameSave.md#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x1221 - 0x1222 - Message Auto-Advance Settings  
  (a padded bool (1 byte))
- 0x1221 - 0x1222 - Subtitle Display  
  (false for on, true for off)
  (a padded bool (1 byte))
- 0x125e - 0x125f - Confirm Action Settings  
  (0 - A, 1 - B)  
  (an unsigned char / u8 (1 byte))
- 0x1225 - 0x1226 - Skip event button  
  (0 - plus, 1 - X)  
  (an unsigned char / u8 (1 byte))
- 0x124c - 0x124d - Game-wide [DLC info](GameSave.md#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x125e - 0x125f - Pause When Resuming Game  
  (a padded bool (1 byte))
