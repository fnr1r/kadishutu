from kadishutu.data.alignment import ALIGNMENT_OFFSET_MAP, AlignmentByte
from typing import Optional, Union

from ..shared.file_handling import BaseDynamicEditor, BaseStaticEditor


class AlignmentEditor(BaseDynamicEditor):
    schema: Optional[AlignmentByte]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.schema = ALIGNMENT_OFFSET_MAP[self.offset]
        except KeyError:
            self.schema = None

    @staticmethod
    def calc_flag(bit: int) -> int:
        return 1 << bit

    @property
    def byte(self) -> int:
        return self.data[self.offset]

    @byte.setter
    def byte(self, value: int):
        self.data[self.offset] = value

    def get_flag(self, bit: int, skip_schema_check: bool = False) -> bool:
        if (not skip_schema_check and
            self.schema and
            not self.schema.has_bit(bit)):
            raise ValueError(f"Bit {bit} not in schema.")
        flag = self.calc_flag(bit)
        return (self.byte & flag) == flag

    def set_flag(
        self,
        bit: int,
        value: bool,
        skip_schema_check: bool = False
    ):
        if (not skip_schema_check and
            self.schema and
            not self.schema.has_bit(bit)):
            raise ValueError(f"Bit {bit} not in schema.")
        flag = self.calc_flag(bit)
        if value:
            self.byte |= flag
        else:
            self.byte &= ~flag

    def __getitem__(self, index: Union[int, str]) -> bool:
        if isinstance(index, int):
            return self.get_flag(index)
        elif isinstance(index, str):
            raise NotImplementedError

    def __setitem__(self, index: Union[int, str], value: bool):
        if isinstance(index, int):
            self.set_flag(index, value)
        elif isinstance(index, str):
            raise NotImplementedError


class AlignmentManager(BaseStaticEditor):
    offset = 0

    def at_offset(self, offset: int) -> AlignmentEditor:
        return self.dispatch(AlignmentEditor, offset)

    def __getitem__(self, offset: int) -> AlignmentEditor:
        return self.at_offset(offset)

    def clear(self):
        for offset in ALIGNMENT_OFFSET_MAP:
            self[offset].byte = 0
