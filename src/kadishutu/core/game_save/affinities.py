from kadishutu.data.affinity import Affinity

from ..shared.editors import (
    BaseDynamicEditor, BaseStructAsFieldEditor, U16Editor,
)


ELEMENTAL_AFFINITY_NAMES = [
    "Physical", "Fire", "Ice", "Electric", "Force", "Light", "Dark",
]

AILMENT_AFFINITY_NAMES = [
    "Poison", "Confusion", "Charm", "Sleep", "Seal", "Mirage",
]


class AffinityEditor(U16Editor):
    def read(self) -> Affinity:
        return Affinity(super().read())
    
    def write(self, v: Affinity):
        super().write(v.value)

    def __get__(self, instance, _) -> Affinity:
        return super().__get__(instance, _)

    def __set__(self, instance, v: Affinity):
        super().__set__(instance, v)


class ElementalAffinityEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = AffinityEditor.fmt

    physical = AffinityEditor(0)
    fire = AffinityEditor(2)
    ice = AffinityEditor(4)
    electric = AffinityEditor(8)
    force = AffinityEditor(10)
    light = AffinityEditor(12)
    dark = AffinityEditor(14)


class AilmentAffinityEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = AffinityEditor.fmt

    poison = AffinityEditor(0)
    confusion = AffinityEditor(4)
    charm = AffinityEditor(6)
    sleep = AffinityEditor(8)
    seal = AffinityEditor(10)
    mirage = AffinityEditor(24)


class AffinityManager(BaseDynamicEditor):
    """
    NOTE: The copies of affinities seem to be the original ones.
    """

    original_elemental = ElementalAffinityEditor.rdisp(0)
    ailment = AilmentAffinityEditor.rdisp(0x10)
    current_elemental = ElementalAffinityEditor.rdisp(0x38)
