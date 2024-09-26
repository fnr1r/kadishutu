from typing import List
from ..shared.editors import BaseStaticEditor, SingularStructEditor, StructEditor, U32Editor
from ..shared.unreal import UE_SAVEGAME_FILE_TYPE_TAG_INT, FCustomVersion, FEngineVersion, extract_fstring


CUSTOM_VERSION_FORMAT = 3
CUSTOM_VERSIONS = 0x37


class FStringEditor(SingularStructEditor):
    fmt = "<i"

    def read(self) -> str:
        length = super().read()
        txt = extract_fstring(
            self.data,
            self.offset + self.struct_obj.size,
            length,
        )
        return txt
    
    def write(self, v):
        raise NotImplementedError("This type of data should not be written")


class FEngineVersionEditor(StructEditor):
    fmt = "<HHHIi"

    def read(self) -> FEngineVersion:
        args = list(self.struct_obj.unpack_from(self.data, self.offset))
        txt = extract_fstring(
            self.data,
            self.offset + self.struct_obj.size,
            args.pop(),
        )
        assert len(args) == 4
        return FEngineVersion(*args, txt)
    
    def write(self, v):
        raise NotImplementedError("This type of data should not be written")


class CustomVersionsEditor(BaseStaticEditor):
    offset = 0x71
    length = U32Editor(0)

    def versions(self) -> List[FCustomVersion]:
        ENTRY_SIZE = 0x14
        return [
            FCustomVersion.from_bytearray(self.data[
                self.offset + ENTRY_SIZE * i:self.offset + ENTRY_SIZE * (i + 1)
            ])
            for i in range(self.length)
        ]


class UnrealInternalEditor(BaseStaticEditor):
    offset = 0x40
    gsav_magic = U32Editor(0)
    gsav_version = U32Editor(0x4)
    package_file_version = U32Editor(0x8)
    engine_version = FEngineVersionEditor(0xc)
    custom_version_format = U32Editor(0x1d)
    custom_versions = CustomVersionsEditor.disp()
    save_game_class_name = FStringEditor(0x481)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.gsav_magic == UE_SAVEGAME_FILE_TYPE_TAG_INT
