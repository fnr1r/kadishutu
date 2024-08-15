from enum import Enum, auto


class Element(Enum):
    Physical = 0
    Fire = auto()
    Ice = auto()
    Electric = auto()
    Force = auto()
    Light = auto()
    Dark = auto()
    Almighty = auto()
    Ailment = auto()
    Support = auto()
    Recovery = auto()
    Misc = auto()
    Passive = 12
    Booster = 14
    KeyItem = 15
    Relic = 16
    PressTurn = 17
    Guard = 19
    Talk = 20
    Escape = 22
    Pass = 23
    Mirage = 27
    Sleep = 28
    Confusion = 29
    Charm = 30
    Seal = 31
    Poison = 32
    Mud = 33
    WhitePerson = 34
    RedPerson = 35
    PhysicalBlock = 41
    FireBlock = auto()
    IceBlock = auto()
    ElectricBlock = auto()
    WindBlock = auto()
    LightBlock = auto()
    DarkBlock = auto()
    AttackUpBy1 = 48
    AttackUpBy2 = auto()
    DefenseUpBy1 = auto()
    DefenseUpBy2 = auto()
    HitEvUpBy1 = auto()
    HitEvUpBy2 = auto()
    AttackDownBy1 = auto()
    AttackDownBy2 = auto()
    DefenseDownBy1 = auto()
    DefenseDownBy2 = auto()
    HitEvDownBy1 = auto()
    HitEvDownBy2 = auto()
    PhysicalRepel = 60
    MagicRepel = auto()
    DamageReduction = 62
    Charge = 63
    Concentrate = 64
    RecoveryBoost = 66
    Pierce = 66
    Taunt = 68
    Magatsuhi = auto()
    Succession = 70
    Weak = 72
    Neutral = auto()
    Resist = auto()
    Null = auto()
    Repel = auto()
    Drain = auto()
