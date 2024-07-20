ITEM_TABLE_OFFSET = 0x4c72

# 0x4c72 - 0
# 0x4c73 - 1
# etc...


BUILTIN_ITEM_TABLE = [
    {"id":  1, "name": "Life Stone", "limit": 50},
    {"id":  2, "name": "Chakra Drop", "limit": 30},
    {"id":  3, "name": "Chakra Pot", "limit": 10},
    {"id":  4, "name": "Bead", "limit": 10,
     "desc": "Full HP recovery to 1 ally."},
    {"id":  5, "name": "Bead Chain", "limit": 5,
     "desc": "Full HP recovery to all allies."},
    {"id":  6, "name": "Soma", "limit": 5,
     "desc": "Full HP and MP recovery to 1 ally."},
    {"id": 11, "name": "Medicine", "limit": 50},
    {"id": 12, "name": "Ox Bezoar", "limit": 30},
    {"id": 13, "name": "Ambrosia", "limit": 20},
    {"id": 14, "name": "Muscle Drink", "limit": 10,
     "desc": "Recovers beyond MAX HP to 1 ally but has a chance to inflict Charm/Confusion/Mirage."},
    {"id": 15, "name": "Life Stone Chain", "limit": 20,
     "desc": "Sligh HP recovery to all allies."},
    {"id": 16, "name": "Soma Drop", "limit": 10,
     "desc": "Moderate HP and MP recovery to 1 ally."},
]

def add_attack_items():
    id = 17
    def a(name: str):
        BUILTIN_ITEM_TABLE.append({
            "id": id,
            "name": name,
            "limit": 10,
        })
    types = ["Fire", "Ice", "Elec", "Force", "Light", "Dark"]
    for suffix in ["Shard", "Gem"]:
        for prefix in types:
            a(f"{prefix} {suffix}")
            id += 1
    # last no: 29


add_attack_items()


# KNOWN ID: 0x4c8f - 29
# NOT IN USE: 0x4c8f - 0x4c96 / 29 - 36


BUILTIN_ITEM_TABLE.extend([
    # Ailment Gems
    {"id": 37, "name": "Poison Gem", "limit": 20},
    {"id": 38, "name": "Sleep Gem", "limit": 20},
    {"id": 39, "name": "Confusion gem", "limit": 20},
    {"id": 40, "name": "Mirage Gem", "limit": 20},
    {"id": 41, "name": "Seal Gem", "limit": 20},
    {"id": 42, "name": "Charm Gem", "limit": 20},
    # Support Gems
    {"id": 43, "name": "Charge Gem", "limit": 20},
    {"id": 44, "name": "Concentrate Gem", "limit": 20},
    {"id": 45, "name": "Critical Gem", "limit": 20},
    {"id": 46, "name": "Spirit Drain Gem", "limit": 20},
    {"id": 47, "name": "Life Drain Gem", "limit": 20},
    # NOT IN USE: 48 - 49
    {"id": 50, "name": "Purge Charm", "limit": 10},
    {"id": 51, "name": "Dispel Charm", "limit": 10},
    {"id": 52, "name": "Attack Mirror", "limit": 10},
    {"id": 53, "name": "Magic Mirror", "limit": 10},
    # NOT IN USE: 54
    {"id": 55, "name": "Spyglass", "limit": 50},
    # NOT IN USE: 56 - 58
    {"id": 59, "name": "Gold Card", "limit": 5},
    {"id": 60, "name": "Whittled Goat", "limit": 1},
    {"id": 61, "name": "Smoke Ball", "limit": 10},
    {"id": 62, "name": "Phys Dampener", "limit": 3},
    {"id": 63, "name": "Fire Dampener", "limit": 3},
    {"id": 64, "name": "Ice Dampener", "limit": 3},
    {"id": 65, "name": "Elec Dampener", "limit": 3},
    {"id": 66, "name": "Force Dampener", "limit": 3},
    {"id": 67, "name": "Light Dampener", "limit": 3},
    {"id": 68, "name": "Dark Dampener", "limit": 3},
    # NOT IN USE: 69
    {"id": 70, "name": "Return Pillar", "limit": 1},
    # NOT IN USE: 71
    {"id": 72, "name": "Attract Pipe", "limit": 20},
    {"id": 73, "name": "Miracle Ice", "limit": 1},
    {"id": 74, "name": "Chakra Elixir", "limit": 1},
    {"id": 75, "name": "Curative Cattail", "limit": 1},
    {"id": 76, "name": "Soul-Return", "limit": 1},
    {"id": 77, "name": "Blessed Fan", "limit": 1},
    {"id": 78, "name": "Eye of Balor", "limit": 1},
    {"id": 79, "name": "Spyscope", "limit": 1},
    {"id": 80, "name": "Haraedo Bead", "limit": 1},
    {"id": 81, "name": "Gleam Grenade", "limit": 1},
    {"id": 82, "name": "Gospel"},
    {"id": 83, "name": "Grimore"},
])


def add_growth_items():
    id = 84
    def a(name: str):
        BUILTIN_ITEM_TABLE.append({
            "id": id,
            "name": name,
        })
    stats = [
        "Health", "Stamina", "Strength", "Vitality", "Magic", "Agility", "Luck"
    ]
    for suffix in ["Balm", "Incense"]:
        for prefix in stats:
            a(f"{prefix} {suffix}")
            id += 1
    types = [
        "Battle", "Fire", "Ice", "Elec", "Force", "Light", "Dark",
        "Destruction", "Healing", "Calamity", "Aiding"
    ]
    for t in types:
        a(f"{t} Sutra")
        id += 1
    # last no: 109


add_growth_items()


BUILTIN_ITEM_TABLE.extend([
    {"id": 109, "name": "Small Glory Crystal"},
    {"id": 110, "name": "Big Glory Crystal"},
    {"id": 111, "name": "Small Demon Box"},
    {"id": 112, "name": "Lavish Demon Box"},
    {"id": 113, "name": "New Testament Tablet"},
    # NOT IN USE: 114 - 220 ???
])


RELIC_TABLE_OFFSET = 0x4eda
# NOTE: Relative to Fortune
# TODO: Find true relic table offset


BUILTIN_RELIC_TABLE = [
    {"id": 0, "name": "Fortune"}, # 0x4eda
    # 0x4ee2: Anime Paperweight
    # 0x4ee3: Simple Undershirt
    # 0x4ee4: Segata III Game Console
    # 0x4ee5: Mouse Mummy
    # 0x4ee6: Telephone Card
    # 0x4ee7: Can of Oden
    # 0x4eee: Balloon Value Pack
    # 0x4eff: Marble Bottle
    # 0x4f00: Maid Costume
    # 0x4f01: Golden Triangle
    # id 39
    # Last
    # NOT IN USED: 53 - 80
]
