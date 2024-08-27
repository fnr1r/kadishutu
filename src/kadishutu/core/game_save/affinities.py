from kadishutu.data.affinity import Affinity

from ..shared.file_handling import (
    BaseDynamicEditor, BaseStructAsFieldEditor, structproperty,
)


AFFINITY_NAMES = [
    "Physical", "Fire", "Ice", "Electric", "Force", "Light", "Dark",
    "Poison", "Confusion", "Charm", "Sleep", "Seal", "Mirage"
]


def affinityprop(fmt):
    return structproperty(
        Affinity, fmt,
        lambda u: Affinity(u),
        lambda t: t.value,
    )


class AffinityEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    """
    NOTE: The copies of affinities seem to be the original ones.
    """

    struct = "<H"

    @affinityprop(struct)
    def original_physical(self) -> int:
        return self.field_as_absolute_offset(0)
    @affinityprop(struct)
    def original_fire(self) -> int:
        return self.field_as_absolute_offset(1)
    @affinityprop(struct)
    def original_ice(self) -> int:
        return self.field_as_absolute_offset(2)
    @affinityprop(struct)
    def original_electric(self) -> int:
        return self.field_as_absolute_offset(3)
    @affinityprop(struct)
    def original_force(self) -> int:
        return self.field_as_absolute_offset(4)
    @affinityprop(struct)
    def original_light(self) -> int:
        return self.field_as_absolute_offset(5)
    @affinityprop(struct)
    def original_dark(self) -> int:
        return self.field_as_absolute_offset(6)
    @affinityprop(struct)
    def poison(self) -> int:
        return self.field_as_absolute_offset(8)
    @affinityprop(struct)
    def confusion(self) -> int:
        return self.field_as_absolute_offset(10)
    @affinityprop(struct)
    def charm(self) -> int:
        return self.field_as_absolute_offset(11)
    @affinityprop(struct)
    def sleep(self) -> int:
        return self.field_as_absolute_offset(12)
    @affinityprop(struct)
    def seal(self) -> int:
        return self.field_as_absolute_offset(13)
    @affinityprop(struct)
    def mirage(self) -> int:
        return self.field_as_absolute_offset(20)
    @affinityprop(struct)
    def physical(self) -> int:
        return self.field_as_absolute_offset(28)
    @affinityprop(struct)
    def fire(self) -> int:
        return self.field_as_absolute_offset(29)
    @affinityprop(struct)
    def ice(self) -> int:
        return self.field_as_absolute_offset(30)
    @affinityprop(struct)
    def electric(self) -> int:
        return self.field_as_absolute_offset(31)
    @affinityprop(struct)
    def force(self) -> int:
        return self.field_as_absolute_offset(32)
    @affinityprop(struct)
    def light(self) -> int:
        return self.field_as_absolute_offset(33)
    @affinityprop(struct)
    def dark(self) -> int:
        return self.field_as_absolute_offset(34)
