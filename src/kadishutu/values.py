from enum import Enum


class Difficulty(Enum):
    # Godborn = ???
    Hard = 0b1111100101110101
    Normal = 0b0001010101110110
    Casual = 0b0010000101110110
    Safety = 0b0011000001110110
