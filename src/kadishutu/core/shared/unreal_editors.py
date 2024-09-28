from typing import List
from ..shared.editors import (
    BaseStaticEditor, EditorGetter, SingularStructEditor, StructEditor, U32Editor,
)
from ..shared.unreal import (
    UE_SAVEGAME_FILE_TYPE_TAG_INT, FCustomVersion, FEngineVersion,
    extract_fstring,
)


CUSTOM_VERSION_FORMAT = 3
CUSTOM_VERSIONS = 0x37


def assert_equal_hex(assumed: int, actual: int):
    assert assumed == actual, "{} != {}".format(
        hex(assumed), hex(actual)
    )


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

    def get_end_offset(self) -> int:
        txt_len = super().read()[-1]
        return self.offset + self.struct_obj.size + txt_len


class DynMixin(EditorGetter):
    def __init__(self):
        super().__init__(-1)
    @property
    def offset(self) -> int:
        raise NotImplementedError
    def _offset(self, attr: str) -> int:
        editor = self.editor
        assert isinstance(editor, UnrealInternalEditor)
        ev = getattr(editor.__class__, attr)
        ev._editor = self.editor
        off = ev.get_end_offset()
        assert_equal_hex(self.editor.offset + 0x2d, off)
        return off


class DynU32Editor(U32Editor, DynMixin):
    @property
    def offset(self) -> int:
        self.roffset = 0x1d
        return self._offset("engine_version")


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
    custom_version_format = DynU32Editor()
    custom_versions = CustomVersionsEditor.disp()
    save_game_class_name = FStringEditor(0x481)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.gsav_magic == UE_SAVEGAME_FILE_TYPE_TAG_INT
