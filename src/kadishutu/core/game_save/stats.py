from ..shared.file_handling import (
    BaseDynamicEditor, BaseStructAsFieldEditor, structproperty,
)


STATS_NAMES = ["HP", "MP", "Strength", "Vitality", "Magic", "Agility", "Luck"]


class StatsEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert not self.struct_obj.unpack_from(self.data, self.field_as_absolute_offset(7))[0], \
            "Supposed NULL is not a null????"

    @structproperty(int, struct)
    def hp(self):
        return self.field_as_absolute_offset(0)

    @structproperty(int, struct)
    def mp(self):
        return self.field_as_absolute_offset(1)

    @structproperty(int, struct)
    def strength(self):
        return self.field_as_absolute_offset(2)

    @structproperty(int, struct)
    def vitality(self):
        return self.field_as_absolute_offset(3)

    @structproperty(int, struct)
    def magic(self):
        return self.field_as_absolute_offset(4)

    @structproperty(int, struct)
    def agility(self):
        return self.field_as_absolute_offset(5)

    @structproperty(int, struct)
    def luck(self):
        return self.field_as_absolute_offset(6)


class StatBlockEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<HHHHHHHH"

    @property
    def base(self) -> StatsEditor:
        return self.field_dispatch(StatsEditor, 0)
    @property
    def changes(self) -> StatsEditor:
        return self.field_dispatch(StatsEditor, 1)
    @property
    def current(self) -> StatsEditor:
        return self.field_dispatch(StatsEditor, 2)
    def max_with_sbis(self):
        target = 999
        changes = self.changes
        current = self.current
        for stat in ["strength", "vitality", "magic", "agility", "luck"]:
            inc = target - current.__getattribute__(stat)
            print(f"Using {inc} {stat} boosting items.")
            changes.__setattr__(stat, inc)
            current.__setattr__(stat, target)

    def recalculate(self):
        # TODO: Take skills into account
        for stat in STATS_NAMES:
            stat = stat.lower()
            base = self.base.__getattribute__(stat)
            changes = self.changes.__getattribute__(stat)
            self.current.__setattr__(stat, base + changes)


class HealableEditor(BaseDynamicEditor, BaseStructAsFieldEditor):
    struct = "<H"

    @structproperty(int, struct)
    def hp(self) -> int:
        return self.field_as_absolute_offset(0)
    @structproperty(int, struct)
    def mp(self) -> int:
        return self.field_as_absolute_offset(1)
