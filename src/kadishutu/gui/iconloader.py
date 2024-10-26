from dataclasses import dataclass
from kadishutu.paths import APPDIRS
from pathlib import Path
from typing import Dict
from typing_extensions import Self
from PIL.Image import Image, open as open_image
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap

from kadishutu.data.element_icons import Element
from kadishutu.tools.eprint import eprint, printexcept


UMODEL_EXPORT_PATH = APPDIRS.data_path / "game_data_export"


@dataclass
class ImagePak:
    image: Image
    pixmap: QPixmap
    icon: QIcon

    @classmethod
    def from_image(cls, img: Image) -> Self:
        pix = QPixmap.fromImage(ImageQt(img))
        icon = QIcon()
        icon.addPixmap(pix)
        return cls(img, pix, icon)

    @property
    def size(self) -> QSize:
        return self.pixmap.size()

    def size_div(self, x: int) -> QSize:
        size = self.size
        width = size.width()
        height = size.height()
        if (width % x != 0 or
            height % x != 0):
            raise ValueError("Bad scale {} for width {} height {}".format(
                x, width, height
            ))
        return QSize(width // x, height // x)


class IconLoaderPaths:
    CHARACTER_ICON = "Game/Design/UI/CharaIcon/Textures/dev{id:03}.tga"
    MINI_CHARACTER_ICON = "Game/Design/UI/CharaIcon/Textures/face_all_001.tga"
    ELEMENT_ICONS = "Game/Design/UI/Icon/Element/Textures/icon_element_01.tga"
    LOADING_CHARACTER_ICON = "Game/Design/UI/LoadingCharaIcon/dev_L_{id:03}.tga"

    def character_icon(self, id: int) -> Path:
        return UMODEL_EXPORT_PATH / self.CHARACTER_ICON.format(id=id)

    @property
    def mini_character_icon(self) -> Path:
        return UMODEL_EXPORT_PATH / self.MINI_CHARACTER_ICON

    @property
    def element_icons(self) -> Path:
        return UMODEL_EXPORT_PATH / self.ELEMENT_ICONS

    def loading_character_icon(self, id: int) -> Path:
        return UMODEL_EXPORT_PATH / self.LOADING_CHARACTER_ICON.format(id=id)


class DisabledError(Exception):
    pass


class IconLoader:
    def __init__(self) -> None:
        if not UMODEL_EXPORT_PATH.exists():
            self.disabled = True
            print(
                "{} does not exist. The image loader is disabled."
                .format(UMODEL_EXPORT_PATH)
            )
            return
        self.disabled = False
        self.paths = IconLoaderPaths()
        self.char_icon_map: Dict[int, ImagePak] = {}
        self.mini_char_icon_map: Dict[int, ImagePak] = {}
        self.element_icon_map: Dict[Element, ImagePak] = {}
        self.loading_char_icon_map: Dict[int, ImagePak] = {}

    def assert_not_disabled(self):
        if self.disabled:
            raise DisabledError("The icon loader is disabled")

    @staticmethod
    def assert_is_a_demon(id: int):
        if id == 0xffff:
            raise ValueError

    def character_icon(self, id: int) -> ImagePak:
        self.assert_not_disabled()
        self.assert_is_a_demon(id)
        try:
            return self.char_icon_map[id]
        except KeyError:
            pass
        path = self.paths.character_icon(id)
        imgfile = open_image(path)
        (width, height) = imgfile.size
        crop_hor = 100
        crop_ver = 40
        box = (crop_hor, crop_ver, width - crop_hor, height - crop_ver)
        img = imgfile.crop(box)
        self.char_icon_map[id] = pak = ImagePak.from_image(img)
        return pak

    def mini_character_icon(self, id: int) -> ImagePak:
        self.assert_not_disabled()
        self.assert_is_a_demon(id)
        try:
            return self.mini_char_icon_map[id]
        except KeyError:
            pass
        if not hasattr(self, "mini_char_icon_img"):
            self.mini_char_icon_img = open_image(self.paths.mini_character_icon)
        if not self.mini_char_icon_img:
            raise ValueError("File failed to load initially")
        imgfile = self.mini_char_icon_img
        width = 80
        height = 64
        MINI_CHAR_COLUMNS = 25
        (column, row) = divmod(id, MINI_CHAR_COLUMNS)
        x1 = width * row
        x2 = x1 + width
        y1 = height * column
        y2 = y1 + height
        box = (x1, y1, x2, y2)
        img = imgfile.crop(box)
        self.mini_char_icon_map[id] = pak = ImagePak.from_image(img)
        return pak

    def element_icon(self, element: Element) -> ImagePak:
        self.assert_not_disabled()
        try:
            return self.element_icon_map[element]
        except KeyError:
            pass
        if not hasattr(self, "element_icons_img"):
            self.element_icons_img = open_image(self.paths.element_icons)
        if not self.element_icons_img:
            raise ValueError("File failed to load initially")
        imgfile = self.element_icons_img
        width = height = 84
        id = element.value
        ELEMENT_CHAR_COLUMNS = 12
        (column, row) = divmod(id, ELEMENT_CHAR_COLUMNS)
        x1 = width * row
        x2 = x1 + width
        y1 = height * column
        y2 = y1 + height
        box = (x1, y1, x2, y2)
        img = imgfile.crop(box)
        self.element_icon_map[element] = pak = ImagePak.from_image(img)
        return pak

    def loading_character_icon(self, id: int) -> ImagePak:
        self.assert_not_disabled()
        self.assert_is_a_demon(id)
        try:
            return self.loading_char_icon_map[id]
        except KeyError:
            pass
        path = self.paths.loading_character_icon(id)
        img = open_image(path)
        self.loading_char_icon_map[id] = pak = ImagePak.from_image(img)
        return pak

    @property
    def no_icon(self) -> QIcon:
        return QIcon()


ICON_LOADER = IconLoader()


def handle_image_loading_error(e: Exception, image_ty: str, *args):
    if isinstance(e, DisabledError):
        return
    if isinstance(e, FileNotFoundError):
        eprint(f"No {image_ty} for params {args}")
        return
    printexcept(image_ty, e)
