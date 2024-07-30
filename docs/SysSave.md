# SysSave

Size: 4832 bytes (end at 0x12e0)

Contains settings and some misc data.

## Decryption

Same as for game saves. Chech out [GameSave.md](GameSave.md#decryption) for more info.

## Structure

- 0x0 - 0x20 - SHA1 Hash of the rest of the file  
  (20 bytes)
- 0x5e0 - 0x5f0 - [Volume Sliders](#volume-sliders)  
  (16 bytes)
- 0x5f6 - 0x5f7 - [Horizontal Camara Settings](#hv-camera)  
  (an unsigned char / u8 (1 byte))
- 0x5f7 - 0x5f8 - [Vertical Camara Settings](#hv-camera)  
  (an unsigned char / u8 (1 byte))
- 0x5ff - 0x600 - [Message speed](#message-speeds)  
  (an unsigned char / u8 (1 byte))
- 0x600 - 0x601 - [Minimap Display](#visibility-options)  
  (an unsigned char / u8 (1 byte))
- 0x601 - 0x602 - [Party Panels Display in the Field](#visibility-options)  
  (an unsigned char / u8 (1 byte))
- 0x602 - 0x603 - [Help Display](#visibility-options)  
  (an unsigned char / u8 (1 byte))
- 0x604 - 0x605 - Battle Cursor Memory  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x605 - 0x606 - Auto-Battle Confirmation  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x606 - 0x607 - Party Panels Display During Skills  
  (false for Display, true for Hide)  
  (a padded bool (1 byte))
- 0x608 - 0x609 - Mitama Dance of Glory  
  (a padded bool (1 byte))
- 0x609 - 0x60a - Mitama Dance of Wealth  
  (a padded bool (1 byte))
- 0x60a - 0x60b - Mitama Dance of EXP  
  (a padded bool (1 byte))
- 0x60b - 0x60c - [DLC Flags](GameSave.md#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x61b - 0x61c - Voice Language  
  (0 - Japanese, 1 - English)  
  (an unsigned char / u8 (1 byte))
- 0x61c - 0x61d - [Camera Speed](#camera-speeds)  
  (an unsigned char / u8 (1 byte))
- 0x1220 - 0x1221 - Message Auto-Advance Settings  
  (a padded bool (1 byte))
- 0x1221 - 0x1222 - Subtitle Display  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x1222 - 0x1224 - Analogue Stick Sensitivity  
  (a value from 0 - 10)  
  (an unsigned char / u8 (1 byte))
- 0x1225 - 0x1226 - Skip Event Settings  
  (0 - plus, 1 - X)  
  (an unsigned char / u8 (1 byte))
- 0x1227 - 0x1228 - Camera Angle  
  (0 - Narrow, 1 - Standard, 3 - Wide)  
  (an unsigned char / u8 (1 byte))
- 0x1228 - 0x1229 - [Magatsuhi Gauge Display](#visibility-options)  
  (an unsigned char / u8 (1 byte))
- 0x1229 - 0x122a - Minimap Rotation  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x122a - 0x122b - [L Action](#stick-actions)  
  (an unsigned char / u8 (1 byte))
- 0x122b - 0x122c - [R Action](#stick-actions)  
  (an unsigned char / u8 (1 byte))
- 0x122c - 0x122d - Estoma Field Confirmation  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x122d - 0x122e - Obstacle Opacity  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x122e - 0x122f - [Battle Item Sorting](#sorting-settings)  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x122f - 0x1230 - [Types of Auto-Battle](#types-of-auto-battle)  
  (an unsigned char / u8 (1 byte))
- 0x1230 - 0x1231 - [Skill Animation Speed (Normal)](#skill-animation-speeds)  
  (an unsigned char / u8 (1 byte))
- 0x1231 - 0x1232 - [Skill Animation Speed (Auto-Battle)](#skill-animation-speeds)  
  (an unsigned char / u8 (1 byte))
- 0x1232 - 0x1233 - Skip Skill Animations Using Confirm  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x1233 - 0x1234 - Field Brightness  
  (a value from 0 - 10)  
  (an unsigned char / u8 (1 byte))
- 0x1234 - 0x1235 - Ambient Occlusion  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x1235 - 0x1236 - Motion Blur  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x1236 - 0x1237 - Anti-Aliasing  
  (false for on, true for off)  
  (a padded bool (1 byte))
- 0x124c - 0x124d - [DLC Flags](GameSave.md#dlc-info)  
  (an unsigned char / u8 (1 byte))
- 0x125c - 0x125d - Screen Brightness  
  (a value from 0 - 10)  
  (an unsigned char / u8 (1 byte))
- 0x125d - 0x125e - Pause When Resuming Game  
  (a padded bool (1 byte))
- 0x125e - 0x125f - Confirm Action Settings  
  (0 - A, 1 - B)  
  (an unsigned char / u8 (1 byte))
- 0x1260 - 0x12e0 - NULL

## Value list

### HV Camera

- 0 - Standard
- 1 - Reverse
- 2 - Off

### Message Speeds

- 0 - slow
- 1 - normal
- 2 - fast

### Visibility Options

- 0 - Display
- 1 - Hide
- 2 - Hide when moving

### Camera Speeds

- 0 - Very Slow
- 1 - Slow
- 2 - Standard
- 3 - Fast
- 4 - Very Fast
- 5 - Fastest

### Stick Actions

- 0 - None
- 1 - Continuous dash
- 2 - Reset camera

### Sorting Settings

- 0 - Prioritize recovery items
- 1 - Prioritize attack items
- 2 - Prioritize assist items
- 3 - Prioritize special items

### Types of Auto-Battle

- 0 - Auto-Attack
- 1 - Auto-Skill
- 2 - Choose at Start

### Skill animation speeds

- 0 - Standard
- 1 - Double Speed
- 2 - Max Speed
- 3 - Skip

## Volume sliders

Each slider is an unsigned short / u16 (2 bytes) followed by two NULL bytes.

Values are in the following order:

- Voices
- BGM
- Ambient Noise
- Sound Effects

With values ranging from 0x3f80 (MAX) to 0x0000 (MIN).
