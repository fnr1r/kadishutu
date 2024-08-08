from dataclasses import dataclass
import os
from pathlib import Path
from typing import Dict
from typing_extensions import Self
from PIL import Image as ModImage
from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap


try:
    UMODEL_EXPORT_PATH = os.environ["SMTVV_UMODEL_EXPORT"]
except KeyError:
    UMODEL_EXPORT_PATH = ""


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
    CHARACTER_ICON = "/Game/Design/UI/CharaIcon/Textures/dev{id:03}.tga"
    MINI_CHARACTER_ICON = "/Game/Design/UI/CharaIcon/Textures/face_all_001.tga"
    LOADING_CHARACTER_ICON = "/Game/Design/UI/LoadingCharaIcon/dev_L_{id:03}.tga"

    def character_icon(self, id: int) -> Path:
        return Path(UMODEL_EXPORT_PATH + self.CHARACTER_ICON.format(id=id))

    @property
    def mini_character_icon(self) -> Path:
        return Path(UMODEL_EXPORT_PATH + self.MINI_CHARACTER_ICON)

    def loading_character_icon(self, id: int) -> Path:
        return Path(UMODEL_EXPORT_PATH + self.LOADING_CHARACTER_ICON.format(id=id))


class IconLoader:
    def __init__(self) -> None:
        self.paths = IconLoaderPaths()
        self.char_icon_map: Dict[int, ImagePak] = {}
        self.mini_char_icon_map: Dict[int, ImagePak] = {}

    @staticmethod
    def assert_is_a_demon(id: int):
        if id == 0xffff:
            raise ValueError

    def character_icon(self, id: int) -> ImagePak:
        self.assert_is_a_demon(id)
        try:
            pak = self.char_icon_map[id]
        except KeyError:
            path = self.paths.character_icon(id)
            img = ModImage.open(path)
            (width, height) = img.size
            crop_hor = 100
            crop_ver = 40
            box = (crop_hor, crop_ver, width - crop_hor, height - crop_ver)
            img = img.crop(box)
            self.char_icon_map[id] = pak = ImagePak.from_image(img)
        return pak

    def mini_character_icon(self, id: int) -> ImagePak:
        self.assert_is_a_demon(id)
        try:
            return self.mini_char_icon_map[id]
        except KeyError:
            pass
        if not hasattr(self, "mini_char_icon_img"):
            img = ModImage.open(self.paths.mini_character_icon)
            self.mini_char_icon_img = img
        img = self.mini_char_icon_img
        width = 80
        height = 64
        MINI_CHAR_COLUMNS = 25
        column = id // MINI_CHAR_COLUMNS
        row = id % MINI_CHAR_COLUMNS
        x1 = width * row
        x2 = x1 + width
        y1 = height * column
        y2 = y1 + height
        box = (x1, y1, x2, y2)
        img = img.crop(box)
        self.mini_char_icon_map[id] = pak = ImagePak.from_image(img)
        return pak


ICON_LOADER = IconLoader()
