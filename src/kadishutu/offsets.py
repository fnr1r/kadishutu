from dataclasses import dataclass
from struct import Struct
from typing import Any, List, Optional, Union


@dataclass
class DataAtOffset:
    name: str
    offset: int
    _size: Optional[int]
    fmt: Optional[Struct]
    fields: Optional[str]
    transformer: Optional[Any]

    @classmethod
    def from_size(cls, name: str, offset: int, size: int):
        return cls(name, offset, size, None, None, None)

    @classmethod
    def from_formatstr(cls, name: str, offset: int, format: Union[str, bytes], fields: Optional[str] = None, transformer = None):
        assert format[0] in ["<", ">"], "Endianess is ambigiuous"
        return cls(name, offset, None, Struct(format), fields, transformer)

    @property
    def size(self) -> int:
        if self.fmt:
            return self.fmt.size
        else:
            assert self._size is not None
            return self._size

    @property
    def end_offset(self) -> int:
        return self.offset + self.size

    def unpack(self, buf: bytes) -> Any:
        if not self.fmt:
            return buf
        unpacked = self.fmt.unpack(buf)
        res: Any
        if self.fields:
            res = {}
            for (k, v) in zip(self.fields.split(" "), unpacked):
                res[k] = v
        elif len(unpacked) == 1:
            res = unpacked[0]
        else:
            res = unpacked
        if self.transformer:
            res = self.transformer(res)
        return res


# 12 UTF-16? chars
#META_FIRST_NAME = ("<24s", None, lambda x: str(x, encoding="UTF-16"))
META_FIRST_NAME = ("<24s",)
# 10 UTF-16? chars
#META_LAST_NAME = ("<20s", None, lambda x: str(x, encoding="UTF-16"))
META_LAST_NAME = ("<20s",)
META_STATS = ("<HHHHHHHH", "HP MP ST VI MA AG LU NULL")
META_STATS_HEALABLE = ("<HH", "HP MP")
META_SKILLS = ("<LLLLLLLLLLLLLLLLL", "unk1 S1 unk2 S2 unk3 S3 unk4 S4 unk5 S5 unk6 S6 unk7 S7 unk8 S8")
META_AFFINITIES = ("<HHHHHHH", "PHY FIR ICE ELE FOR LIG DAR")
META_POTENTIALS = ("<hhhhhhhhhhhh", "PHYSICAL FIRE ICE ELECTRIC FORCE LIGHT DARK ALMIGHTY AILMENT SUPPORT HEALING _unknown")


DEMON_TABLE_OFFSET = 0xb60
DEMON_ENTRY_SIZE = 424


a = DataAtOffset.from_formatstr


GAME_SAVE_INFO: List[DataAtOffset] = [
    a("sha1_hash", 0, "<20s"),

    a("first_name1", 0x4d8, *META_FIRST_NAME),

    #a("difficulty", 0x54c, "H"),

    # NOTE: The game saves the time of saving in some weird format.
    a("time_of_saving", 0x4f0, "<QQ"),

    a("play_time", 0x5d0, "<L"),

    a("gui_player_lvl", 0x618, "<B"),

    a("first_name2", 0x9d0, *META_FIRST_NAME),
    a("last_name2", 0x9e8, *META_LAST_NAME),
    a("first_name3", 0x9fc, *META_FIRST_NAME),

    a("stats_initial", 0x988, *META_STATS),
    # NOTE: This does not count Aogami/Tsukuyomi talk events
    a("stats_changes", 0x998, *META_STATS),
    a("stats_current", 0x9a8, *META_STATS),
    # NOTE: Always 4????
    a("stats_mystery_stuff", 0x9b8, "<l"),
    a("stats_healable", 0x9bc, *META_STATS_HEALABLE),
    #FFI("stats2", 0x9c0, "II", "LV EXP"),
    a("player_lvl", 0x9c8, "<B"),

    a("last_name4", 0xa1c, *META_LAST_NAME),

    a("skills", 0xa38, *META_SKILLS),

    a("affinities", 0xa98, *META_AFFINITIES),

    a("potentials", 0xb38, *META_POTENTIALS),

    # DEMON TABLE START: 0xb60
    # DEMON TABLE END (assuming table size 24): 0x3320
    # NOTE: It's possibly +4/5 due to guests
    # Yoko, Tao, Yuzuru, Ichiro and Demi-fiend
    # (although Demi-fiend is not available until the end of the game)
    # UPDATE: The table size seems to be 30

    a("macca", 0x3d32, "<I"),
    a("glory", 0x3d36, "<I"),

    a("summoned_demons", 0x3d2e, "<BBB", "first second third"),
    a("protag_placement", 0x3d45, "<B"),

    a("magatsuhi_gauge", 0x3ece, "<H"),

    ## Consumables
    # Start of table: 0x4c72
    # End of table: ???

    # 0x4da8: NO EFFECT - probably no essence
    ## Essence (1)
    # 0x4da9: Khonsu
    # ...
    # 0x4ebb: Saturnus

    ## Relics
    # 0x4ed0: relic?
    # 0x4f00: Maid Costume

    ## Key Items
    # Start of table: 0x4f02
    # 0x4f02: Golden Apple
    # 0x4f03: Akiha-Gongen Talisman
    # 0x4f04: Key of Austerity
    # 0x4f05: Key of Benevolence
    # 0x4f06: Key of Harmony
    # 0x4f07: Angel Feather
    # 0x4f08: NOT IN USE nr 7
    # 0x4f09: NOT IN USE nr 8
    # 0x4f1f: NOT IN USE nr 30
    # 0x4f62: Heavenly Keystone
    # 0x4f63: Purified Sake
    # 0x4f64: Kiou Sword
    # 0x4f65: Oak Staff
    ## Quest items???
    # 0x4f66: Jatayu Egg
    # 0x4f67: Mandrake Root
    # 0x4f68: Giant Bird's Feather
    # 0x4f69: Shikigami Talisman
    # 0x4f6a: Mothman Capture Pot
    # 0x4f6b: Kumbhanda's Bottle
    # 0x4f6c: Incubus's Letter
    # 0x4f6d: Frozen King Salmon
    # 0x4f6e: Kunitsu Keystone
    # 0x4f6f: Gibbon Guitar
    # 0x4f70: Large Model Kit
    # 0x4f71: TV-Game Combination
    # 0x4f75: Aquamarine
    # 0x4f81 - 0x4f8b: Menorahs (in order)
    # 0x4fc0: Chaos Talisman
    # 0x4fc1 - 0x4fc9: NOT IN USE 192 - 200
    # End of table: 0x4fc9

    ## RELICS AGAIN?!?!?!?!?!
    # 0x4fca: Soup Can (id 40?)
    # 0x4fcb: Dry Cell Battery
    # 0x4fcc: Disposable Camera
    # 0x4fcd: Mini Cartridge
    # 0x4fce: Traveler's Check
    # 0x4fcf: Crowned Bottle
    # 0x4fd6: NOT IN USE nr 53
    # 0x4fe9: NOT IN USE nr 72
    # 0x4ff1: NOT IN USE nr 80
    # End of table: 0x4ff1

    ## Essences (metadata)
    # Start of table: 0x5129
    # 0x5196: Slime
    # 0x5221: Aogami Type-D Essence

    # 00 - Not owned
    # 02 - New
    # 04 - ???? (possible)
    # 06 - Owned
    # 16 - Used

    # TODO: Figure this shit out
    # (It's too close for comfort, oh)
    a("coordinates", 0x568e, "<lll"),
    a("rotation", 0x56a6, "<LL"),

    # 0x7dc0 - 0x7de0: Demon haunt data

    # Tracking
    # NOT TRACKED: Balms and Incenses
    # 0x1375e: Tracks used boxes

    # 0x180f?: Tracks used essences

    # 0x69a90: Settings
    #a("settings_mitama", 0x69a90, "<B"),
    # 0x6a07f: DLC Flags???
]

del a

for i in range(24):
    current_offset = DEMON_TABLE_OFFSET + DEMON_ENTRY_SIZE * i

    def add_dat(subname: str, relative_offset: int, *args):
        GAME_SAVE_INFO.append(DataAtOffset.from_formatstr(
            "demon_{}_{}".format(str(i).zfill(2), subname),
            current_offset + relative_offset,
            *args
        ))
    add_dat("stats_initial", 0, *META_STATS)
    add_dat("stats_changes", 16, *META_STATS)
    add_dat("stats_current", 32, *META_STATS)
    # end: 48

    #add_dat("x_magic_number", 64, "<l")
    add_dat("friendship", 68, "<L")
    add_dat("maybe_is_summoned", 72, "<H")
    add_dat("dh_talks", 74, "<H")
    # end: 76

    #add_dat("statsx", 84, "<HH")
    add_dat("stats_healable", 100, *META_STATS_HEALABLE)
    add_dat("exp", 104, "<Q")
    add_dat("lvl", 112, "<H")
    add_dat("id", 114, "<H")
    # end: 116

    add_dat("skills", 120, *META_SKILLS)
    # end: 184

    add_dat("affinities", 216, *META_AFFINITIES)
    # end: 230

    add_dat("potentials", 384, *META_POTENTIALS)

    add_dat("innate_skill", 408, "<H")

    GAME_SAVE_INFO.append(DataAtOffset.from_size("raw", 0, DEMON_ENTRY_SIZE))
