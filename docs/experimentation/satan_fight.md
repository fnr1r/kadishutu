# Satan fight changes

## NOTE

This is done on a non-newgame+ savefile via adding all endings and setting
cycle count to 99.

## After Satan is defeated

### AFTER_SATAN_1

0x4982: ??????

0x00 -> 0x02

### Satan's Essence (ITEM)

0x4ea2: Satan's essence

0x00 -> 0x01

### Primal Talisman

0x4fbd: Primal Talisman

0x00 -> 0x01

### Satan's Essence (META)

0x5222: Satan's essence

0x00 -> 0x02

NULL -> New

### AFTER_SATAN_2

0x533d: Primal Talisman... ESSENCE????

0x00 -> 0x02

NULL -> Owned

### MIRACLE_0

0x67f5: ????

0x00 -> 0x01

????

### AFTER_SATAN_3

```txt
00007dc8: 0000 2600  ..&.
00007dcc: a09c 9144  ...D
00007dd0: 852a 48c2  .*H.
00007dd4: 5202 4dc9  R.M.
00007dd8: 2029 1501   )..
00007ddc: 411a 751c  A.u.
00007de0: 8445 49ad  .EI.
00007de4: 0c52 1218  .R..
00007de8: 20c9 8440   ..@
00007dec: 4891 4411  H.D.
00007df0: 2205 0092  "...
00007df4: 4812 2a20  H.* 
00007df8: a550 0801  .P..
00007dfc: 1118 5804  ..X.
00007e00: 0418 0a00  ....
```

```txt
00007dc8: 0000 2500  ..%.
00007dcc: 1094 a282  ....
00007dd0: 1694 c8c0  ....
00007dd4: 2248 4010  "H@.
00007dd8: 0127 44a1  .'D.
00007ddc: 4124 2302  A$#.
00007de0: 2570 2c82  %p,.
00007de4: 9c21 0918  .!..
00007de8: 9028 491a  .(I.
00007dec: a460 2489  .`$.
00007df0: 8888 0a43  ...C
00007df4: 0c94 8420  ... 
00007df8: 0831 0401  .1..
00007dfc: 22a8 8860  "..`
00007e00: 044a 7800  .Jx.
```

### Analyze: Satan data

```txt
0005f728: 0000 0000  ....
0005f72c: 0000 0000  ....
0005f730: 0000 0000  ....
```

```txt
0005f728: 0000 0181  ....
0005f72c: 0000 0080  ....
0005f730: 0001 0000  ....
```

### AFTER_SATAN_4

```txt
0005f758: 0000 0000  ....
```

```txt
0005f758: 0000 0100  ....
```

### AFTER_SATAN_5

```txt
0005f818: 0000 0000  ....
```

```txt
0005f818: 0000 0101  ....
```

???

### AFTER_SATAN_6

```txt
00069abc: 0a02 0aaa  ....
```

```txt
00069abc: 2a02 0aaa  *...
```

### AFTER_SATAN_7

```txt
00069c88: ffde 0800  ....
```

```txt
00069c88: ffdf 0800  ....
```

NOTE: This did not appear in another run.

### MIRACLE_1

```txt
00069ce4: 6f0f 00c4  o...
```

```txt
00069ce4: 6f0f 10c4  o...
```

### Godborn unlock

```txt
0006a068: 5a40 2ff8  Z@/.
```

```txt
0006a068: 5e40 2ff8  ^@/.
```

This unlocks the Godborn option during NG+.

## Shared across saves

### Quest data section

```txt
0005b09c: 0000 0000  ....
0005b0a0: 0000 0000  ....
```

```txt
0005b09c: 0000 0100  ....
0005b0a0: 0000 0000  ....
```

```txt
0005b09c: 0000 0001  ....
0005b0a0: 0000 0100  ....
```

Probably quest data

### ???

```txt
0006a084: e4f7 db10  ....
```

```txt
0006a084: e4f7 dbb0  ....
```

```txt
0006a084: e4f7 dbf0  ....
```

Maybe also quest data?

## Experimentation

### Quest data

```python
## "The Great Adversary" quest data: 0x5b09c
# 0000 0000 - Not started
# 0000 0100 - Started
# 0000 0001 - Completed
## "The Great Adversary": 0x5b0a0
# 0000 0000 -> 0000 0001 - Removed new flag
# 0000 0100 -> 0001 0000 - Removed new and completed flag
## (tired 2 times)
## "The Great Adversary" quest new flag: 0x6a088
# 0xf8 -> 0xfe - Removed new flag
# 0xf8 -> 0xfe - Removed new and completed flag
```

## Attempt 2

### M1

```txt
000004fc: 0361 1204  .a..
```

```txt
000004fc: 03a9 1204  ....
```

```txt
000004fc: 033e 1304  .>..
```

### AFTER_SATAN_1M

```txt
0x4982: ??????

0x00 -> 0x02
```

### ????M

```txt
00007dc8: 0000 2600  ..&.
00007dcc: 1056 4642  .VFB
00007dd0: 2858 04c2  (X..
00007dd4: 1a02 81c5  ....
00007dd8: 902a 4a00  .*J.
00007ddc: 8964 5084  .dP.
00007de0: 2260 d868  "`.h
00007de4: 8919 2118  ..!.
00007de8: 20c5 9018   ...
00007dec: 3118 8620  1.. 
00007df0: 0107 4202  ..B.
00007df4: 830a 1009  ....
00007df8: 1510 0201  ....
00007dfc: 4442 8224  DB.$
00007e00: 4090 1a00  @...
```

```txt
00007dc8: 0000 2640  ..&@
00007dcc: a060 8942  .`.B
00007dd0: 1698 8228  ...(
00007dd4: 4d31 6090  M1`.
00007dd8: 3052 2902  0R).
00007ddc: 06aa 3280  ..2.
00007de0: 8260 3886  .`8.
00007de4: 54a1 1218  T...
00007de8: 9044 4522  .DE"
00007dec: 4812 2a40  H.*@
00007df0: 5204 0202  R...
00007df4: 4311 9208  C...
00007df8: 8910 0342  ...B
00007dfc: 4070 410a  @pA.
00007e00: 4000 3000  @.0.
```

### Quest???

```txt
0005f818: 0000 0000  ....
```

```txt
0005f818: 0000 0100  ....
```

## Analyze data marked as seen

0x5f728: 0000 0180 -> 0000 0380

## Satan essence marked as seen

0x5222: Satan's essence

0x02 -> 0x06

New -> Seen

## Unlocked miracle marked as seen

### A

0x3ddc: 0707 0200 -> 0707 0202

NOTE: This seems to be the end of the miracle block.

### B

0x180d4: 0x01 -> 0x03

## Miracle bought

### B2

0x3ddc: 0707 0202 -> 0707 0207

NOTE: Yes. This is the miracle block.
