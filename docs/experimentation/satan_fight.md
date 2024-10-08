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

### Map data

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

EDIT

Nope. It's map data. Useless for me.

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

## One more time

### Quest rejected

```diff
@@ -108575,7 +108575,7 @@
 0006a078: 4400 00fa  D...
 0006a07c: 0b00 00b8  ....
 0006a080: 0a7f ffff  ....
-0006a084: e4f7 db10  ....
+0006a084: e4f7 db90  ....
 0006a088: fe1f 0100  ....
 0006a08c: 0000 0000  ....
 0006a090: 0000 0000  ....
```

### Quest accepted

```diff
@@ -93221,7 +93221,7 @@
 0005b090: 0000 0000  ....
 0005b094: 0000 0000  ....
 0005b098: 0000 0000  ....
-0005b09c: 0000 0000  ....
+0005b09c: 0000 0100  ....
 0005b0a0: 0000 0000  ....
 0005b0a4: 0000 0000  ....
 0005b0a8: 0000 0000  ....
@@ -108575,7 +108575,7 @@
 0006a078: 4400 00fa  D...
 0006a07c: 0b00 00b8  ....
 0006a080: 0a7f ffff  ....
-0006a084: e4f7 db10  ....
+0006a084: e4f7 dbb0  ....
 0006a088: fe1f 0100  ....
 0006a08c: 0000 0000  ....
 0006a090: 0000 0000  ....
```

### Quest marked as seen

```diff
@@ -93222,7 +93222,7 @@
 0005b094: 0000 0000  ....
 0005b098: 0000 0000  ....
 0005b09c: 0000 0100  ....
-0005b0a0: 0000 0000  ....
+0005b0a0: 0001 0000  ....
 0005b0a4: 0000 0000  ....
 0005b0a8: 0000 0000  ....
 0005b0ac: 0000 0000  ....
```

### Quest completed

```diff
@@ -4702,7 +4702,7 @@
 00004974: 0000 0000  ....
 00004978: 0000 0000  ....
 0000497c: 0000 0000  ....
-00004980: 0000 0000  ....
+00004980: 0000 0200  ....
 00004984: 0000 be00  ....
 00004988: 0100 e000  ....
 0000498c: 0000 9400  ....
@@ -5030,7 +5030,7 @@
 00004e94: 0101 0101  ....
 00004e98: 0101 0101  ....
 00004e9c: 0100 0101  ....
-00004ea0: 0101 0000  ....
+00004ea0: 0101 0100  ....
 00004ea4: 0001 0101  ....
 00004ea8: 0101 0001  ....
 00004eac: 0101 0101  ....
@@ -5101,7 +5101,7 @@
 00004fb0: 0101 0101  ....
 00004fb4: 0101 0101  ....
 00004fb8: 0101 0101  ....
-00004fbc: 0100 0001  ....
+00004fbc: 0101 0001  ....
 00004fc0: 0000 0000  ....
 00004fc4: 0000 0000  ....
 00004fc8: 0000 0000  ....
@@ -5254,7 +5254,7 @@
 00005214: 0606 0606  ....
 00005218: 0606 0606  ....
 0000521c: 0600 0606  ....
-00005220: 0606 0000  ....
+00005220: 0606 0200  ....
 00005224: 0006 0606  ....
 00005228: 0606 0006  ....
 0000522c: 0606 0606  ....
@@ -5325,7 +5325,7 @@
 00005330: 0202 0202  ....
 00005334: 0202 0202  ....
 00005338: 0202 0202  ....
-0000533c: 0200 0002  ....
+0000533c: 0202 0002  ....
 00005340: 0000 0000  ....
 00005344: 0000 0000  ....
 00005348: 0000 0202  ....
@@ -6651,7 +6651,7 @@
 000067e8: 0101 0101  ....
 000067ec: 0101 0100  ....
 000067f0: 0000 0001  ....
-000067f4: 0100 0000  ....
+000067f4: 0101 0000  ....
 000067f8: 0000 0000  ....
 000067fc: 0000 0000  ....
 00006800: 0000 0000  ....
@@ -8048,21 +8048,21 @@
 00007dbc: 0000 0000  ....
 00007dc0: 0000 0000  ....
 00007dc4: 0000 0000  ....
-00007dc8: 0000 2520  ..% 
-00007dcc: 2058 0583   X..
-00007dd0: 890c 11a4  ....
-00007dd4: 3416 8092  4...
-00007dd8: e084 4584  ..E.
-00007ddc: 22a8 040f  "...
-00007de0: 3044 314a  0D1J
-00007de4: e205 2418  ..$.
-00007de8: 9044 0541  .D.A
-00007dec: a410 4610  ..F.
-00007df0: 0947 21a2  .G!.
-00007df4: 2414 0412  $...
-00007df8: 4585 2011  E. .
-00007dfc: 2451 9014  $Q..
-00007e00: 002a 6300  .*c.
+00007dc8: 0000 2500  ..%.
+00007dcc: 9069 8904  .i..
+00007dd0: 2b31 88a2  +1..
+00007dd4: 2415 4841  $.HA
+00007dd8: a928 0942  .(.B
+00007ddc: 8524 4300  .$C.
+00007de0: 51b2 4cb1  Q.L.
+00007de4: 7232 0a18  r2..
+00007de8: 4019 45a4  @.E.
+00007dec: c5a0 4810  ..H.
+00007df0: 0126 2482  .&$.
+00007df4: 2422 4408  $"D.
+00007df8: 0409 4300  ..C.
+00007dfc: 0c10 2a03  ..*.
+00007e00: c418 4900  ..I.
 00007e04: 0000 0000  ....
 00007e08: 0000 0000  ....
 00007e0c: 0000 0000  ....
@@ -93221,8 +93221,8 @@
 0005b090: 0000 0000  ....
 0005b094: 0000 0000  ....
 0005b098: 0000 0000  ....
-0005b09c: 0000 0100  ....
-0005b0a0: 0001 0000  ....
+0005b09c: 0000 0001  ....
+0005b0a0: 0001 0100  ....
 0005b0a4: 0000 0000  ....
 0005b0a8: 0000 0000  ....
 0005b0ac: 0000 0000  ....
@@ -97736,9 +97736,9 @@
 0005f71c: 0000 0000  ....
 0005f720: 0000 0000  ....
 0005f724: 0000 0000  ....
-0005f728: 0000 0000  ....
-0005f72c: 0000 0000  ....
-0005f730: 0000 0000  ....
+0005f728: 0000 0180  ....
+0005f72c: 0000 0080  ....
+0005f730: 0001 0000  ....
 0005f734: 0000 0000  ....
 0005f738: 0000 0000  ....
 0005f73c: 0000 0000  ....
@@ -97748,7 +97748,7 @@
 0005f74c: 0000 0000  ....
 0005f750: 0000 0000  ....
 0005f754: 0000 0000  ....
-0005f758: 0000 0000  ....
+0005f758: 0000 0100  ....
 0005f75c: 0000 0000  ....
 0005f760: 0000 0000  ....
 0005f764: 0000 0000  ....
@@ -97796,7 +97796,7 @@
 0005f80c: 0000 0000  ....
 0005f810: 0000 0000  ....
 0005f814: 0000 0000  ....
-0005f818: 0000 0000  ....
+0005f818: 0000 0100  ....
 0005f81c: 0000 0000  ....
 0005f820: 0000 0000  ....
 0005f824: 0000 0000  ....
@@ -108205,7 +108205,7 @@
 00069ab0: 0000 00a8  ....
 00069ab4: aaaa a08a  ....
 00069ab8: a2aa aaaa  ....
-00069abc: 0a02 0aaa  ....
+00069abc: 2a02 0aaa  *...
 00069ac0: aaa2 0800  ....
 00069ac4: 0000 0000  ....
 00069ac8: 0000 0000  ....
@@ -108343,7 +108343,7 @@
 00069cd8: 7f00 a027  ...'
 00069cdc: 4c80 fff3  L...
 00069ce0: fff3 93ff  ....
-00069ce4: 6f0f 00c4  o...
+00069ce4: 6f0f 10c4  o...
 00069ce8: bb04 18c0  ....
 00069cec: 0300 801f  ....
 00069cf0: 0000 0000  ....
@@ -108568,14 +108568,14 @@
 0006a05c: 0000 0000  ....
 0006a060: 00d0 9100  ....
 0006a064: 0000 7cfe  ..|.
-0006a068: 5a40 2ff8  Z@/.
+0006a068: 5e40 2ff8  ^@/.
 0006a06c: 1f80 ffcf  ....
 0006a070: ff75 5ef8  .u^.
 0006a074: 8377 0608  .w..
 0006a078: 4400 00fa  D...
 0006a07c: 0b00 00b8  ....
 0006a080: 0a7f ffff  ....
-0006a084: e4f7 dbb0  ....
+0006a084: e4f7 dbf0  ....
 0006a088: fe1f 0100  ....
 0006a08c: 0000 0000  ....
 0006a090: 0000 0000  ....
```

### Quest completed + seen

```diff
@@ -93222,7 +93222,7 @@
 0005b094: 0000 0000  ....
 0005b098: 0000 0000  ....
 0005b09c: 0000 0001  ....
-0005b0a0: 0001 0100  ....
+0005b0a0: 0001 0000  ....
 0005b0a4: 0000 0000  ....
 0005b0a8: 0000 0000  ....
 0005b0ac: 0000 0000  ....
```

### Essence + an data seen

```diff
@@ -5254,7 +5254,7 @@
 00005214: 0606 0606  ....
 00005218: 0606 0606  ....
 0000521c: 0600 0606  ....
-00005220: 0606 0200  ....
+00005220: 0606 0600  ....
 00005224: 0006 0606  ....
 00005228: 0606 0006  ....
 0000522c: 0606 0606  ....
@@ -97736,7 +97736,7 @@
 0005f71c: 0000 0000  ....
 0005f720: 0000 0000  ....
 0005f724: 0000 0000  ....
-0005f728: 0000 0180  ....
+0005f728: 0000 0380  ....
 0005f72c: 0000 0080  ....
 0005f730: 0001 0000  ....
 0005f734: 0000 0000  ....
```

### Essence used

```diff
@@ -5030,7 +5030,7 @@
 00004e94: 0101 0101  ....
 00004e98: 0101 0101  ....
 00004e9c: 0100 0101  ....
-00004ea0: 0101 0100  ....
+00004ea0: 0101 0000  ....
 00004ea4: 0001 0101  ....
 00004ea8: 0101 0001  ....
 00004eac: 0101 0101  ....
@@ -5254,7 +5254,7 @@
 00005214: 0606 0606  ....
 00005218: 0606 0606  ....
 0000521c: 0600 0606  ....
-00005220: 0606 0600  ....
+00005220: 0606 1600  ....
 00005224: 0006 0606  ....
 00005228: 0606 0006  ....
 0000522c: 0606 0606  ....
```

### Miracle seen

```diff
@@ -3957,7 +3957,7 @@
 00003dd0: 0702 0707  ....
 00003dd4: 0207 0300  ....
 00003dd8: 0707 0003  ....
-00003ddc: 0707 0200  ....
+00003ddc: 0707 0202  ....
 00003de0: 0000 0000  ....
 00003de4: 0000 0000  ....
 00003de8: 0000 0000  ....
@@ -24627,14 +24627,14 @@
 000180c8: fdff fff7  ....
 000180cc: defb ffff  ....
 000180d0: ffff feed  ....
-000180d4: 0100 0000  ....
+000180d4: 0300 0000  ....
 000180d8: 0000 0000  ....
 000180dc: 0000 0000  ....
 000180e0: 0000 0000  ....
```

### Essence tracking

```diff
 000180e4: 0000 0000  ....
 000180e8: 0000 0000  ....
 000180ec: 0000 0000  ....
-000180f0: 0000 1900  ....
+000180f0: 0000 1a00  ....
 000180f4: 0000 0000  ....
 000180f8: 0000 0000  ....
 000180fc: 0000 0000  ....
```

0x180f2 - Essences used

### Mysterious value

```diff
@@ -4702,7 +4702,7 @@
 00004974: 0000 0000  ....
 00004978: 0000 0000  ....
 0000497c: 0000 0000  ....
-00004980: 0000 0200  ....
+00004980: 0000 0300  ....
 00004984: 0000 be00  ....
 00004988: 0100 e000  ....
 0000498c: 0000 9400  ....
```

```diff
@@ -8048,21 +8048,21 @@
 00007dbc: 0000 0000  ....
 00007dc0: 0000 0000  ....
 00007dc4: 0000 0000  ....
-00007dc8: 0000 2500  ..%.
-00007dcc: 9069 8904  .i..
-00007dd0: 2b31 88a2  +1..
-00007dd4: 2415 4841  $.HA
-00007dd8: a928 0942  .(.B
-00007ddc: 8524 4300  .$C.
-00007de0: 51b2 4cb1  Q.L.
-00007de4: 7232 0a18  r2..
-00007de8: 4019 45a4  @.E.
-00007dec: c5a0 4810  ..H.
-00007df0: 0126 2482  .&$.
-00007df4: 2422 4408  $"D.
-00007df8: 0409 4300  ..C.
-00007dfc: 0c10 2a03  ..*.
-00007e00: c418 4900  ..I.
+00007dc8: 0000 2620  ..& 
+00007dcc: 1092 8542  ...B
+00007dd0: 4444 22c2  DD".
+00007dd4: 1228 40c0  .(@.
+00007dd8: 8284 9444  ...D
+00007ddc: 85a8 9280  ....
+00007de0: 4290 2686  B.&.
+00007de4: 9295 0c18  ....
+00007de8: c092 849c  ....
+00007dec: 4558 1810  EX..
+00007df0: 9186 400c  ..@.
+00007df4: 1112 0406  ....
+00007df8: 6502 8440  e..@
+00007dfc: 0890 6048  ..`H
+00007e00: 005a 6000  .Z`.
 00007e04: 0000 0000  ....
 00007e08: 0000 0000  ....
 00007e0c: 0000 0000  ....
```

## Quest meta analasis


```txt
0x00000000
  01234567
```

0x5b0a0 - 0001 0100

- octet 1 - ???
- octet 2 - seen flag
  (00 - unseen, 01 - seen)
- octet 3 - completed flag
  (01 - flagged, 00 - flag removed)
- octet 4 - ???
