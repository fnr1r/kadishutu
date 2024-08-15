from enum import Enum


class Affinity(Enum):
    Weak = 125
    Neutral = 100
    Resist = 50
    Null = 0
    Repel = 999
    Drain = 1000

    Unknown10 = 10
    Unknown20 = 20
    Unknown40 = 40
    Unknown150 = 150
    Unknown300 = 300
    Unknown900 = 900


def affinity_as_map() -> dict[str, Affinity]:
    res = {}
    for i in Affinity:
        res[Affinity(i).name] = Affinity(i)
    return res


AFFINITY_MAP = affinity_as_map()
