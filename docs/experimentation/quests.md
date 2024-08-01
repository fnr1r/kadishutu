# Quest Data

This file contains info related to finding the quest data offset.

## "The Angel's Request" quest data

From diff 1 (quest started):

- 0x11e6b (an unsigned char / u8 (1 byte))
- 0x5a794 (an unsigned short / u16 (2 bytes))
- 0x69ca9 (an unsigned char / u8 (1 byte))
- 0x69ed6 (an unsigned short / u16 (2 bytes))

From diff 2 (quest conditions met):

- 0x69ca9 (an unsigned char / u8 (1 byte))  
  (does not appear in alignment)
- 0x69edd (an unsigned char / u8 (1 byte))
