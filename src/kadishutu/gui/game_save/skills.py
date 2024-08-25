from abc import abstractmethod
from kadishutu.core.game_save.skills import SkillEditor, SkillManager
from kadishutu.data.element_icons import Element
from kadishutu.data.skills import SKILL_ID_MAP, SKILL_NAME_MAP
from typing import List, Tuple
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QSpinBox, QWidget,
)

from ..shared import QU32, SHIBOKEN_MAX, AppliableWidget, ModifiedMixin
from ..iconloader import ICON_LOADER, print_icon_loading_error
from .shared import GameScreenMixin


class AbstractStrIntMap(QWidget, ModifiedMixin):
    def __init__(self, items: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedMixin.__init__(self)

        self.l = QHBoxLayout(self)
        self.l.setContentsMargins(0, 0, 0, 0)

        self.str_box = QComboBox()
        self.str_box.addItems(items)
        self.str_box.currentTextChanged.connect(self.str_changed)
        self.l.addWidget(self.str_box)

        self.int_box = QSpinBox()
        self.int_box.valueChanged.connect(self.int_changed)
        self.l.addWidget(self.int_box)

    def get_value(self) -> int:
        return self.int_box.value()

    @abstractmethod
    def refresh(self):
        raise NotImplementedError

    @abstractmethod
    def apply_changes(self):
        raise NotImplementedError

    @abstractmethod
    def int_to_str(self, value: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def str_to_int(self, value: str) -> int:
        raise NotImplementedError

    def int_changed(self, value: int):
        self.set_modified(True)
        self.str_box.setCurrentText(self.int_to_str(value))

    def str_changed(self, value: str):
        self.set_modified(True)
        self.int_box.setValue(self.str_to_int(value))


class SkillBox(AbstractStrIntMap, ModifiedMixin):
    NO_VALUE_INT = 0
    NO_VALUE_STR = "NONE"

    def __init__(self, skill: SkillEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.str_box.insertItem(0, self.NO_VALUE_STR)
        ModifiedMixin.__init__(self)
        self.skill = skill
        self.int_box.setMaximum(SHIBOKEN_MAX)

    def refresh(self):
        self.int_box.setValue(self.skill.id)
        if self.skill.id == self.NO_VALUE_INT:
            self.str_box.setCurrentIndex(0)
            return
        self.str_box.setCurrentText(self.skill.name)

    def apply_changes(self):
        if self.get_modified:
            self.skill.id = self.int_box.value()
            self.set_modified(False)

    def int_to_str(self, value: int) -> str:
        if value == self.NO_VALUE_INT:
            return self.NO_VALUE_STR
        return SKILL_ID_MAP[value].name

    def str_to_int(self, value: str) -> int:
        if value == self.NO_VALUE_STR:
            return self.NO_VALUE_INT
        return SKILL_NAME_MAP[value].id


class SkillEditorScreen(QWidget, GameScreenMixin, AppliableWidget):
    def __init__(
        self,
        skills: SkillManager,
        innate_skill: SkillEditor,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.skills = skills
        self.widgets: List[Tuple[SkillBox, QU32]] = []

        self.l = QGridLayout(self)

        all_skills = list(SKILL_NAME_MAP.keys())

        for i in range(9):
            if i == 0:
                skill = innate_skill
                label = QLabel("Innate skill")
            else:
                skill = skills.slot(i - 1)
                label = QLabel(f"Skill {i}")
            self.l.addWidget(label, i, 0)
            skill_box = SkillBox(skill, all_skills)
            self.l.addWidget(skill_box, i, 2)
            mystery_box = QU32()
            self.l.addWidget(mystery_box, i, 4)
            icon = QLabel()
            self.l.addWidget(icon, i, 1)
            mp_cost = QLabel()
            self.l.addWidget(mp_cost, i, 3)
            if not i:
                mystery_box.hide()
                mp_cost.hide()
            cb = self.make_meta_refresh_callback(icon, mp_cost)
            skill_box.int_box.valueChanged.connect(cb)
            self.widgets.append((skill_box, mystery_box))

    def meta_refresh(
        self,
        skill_id: int,
        icon: QLabel,
        mp_cost: QLabel,
    ):
        if skill_id == SkillBox.NO_VALUE_INT:
            mp_cost.hide()
            icon.hide()
            return
        else:
            mp_cost.show()
            icon.show()
        skill_meta = SKILL_ID_MAP[skill_id]
        element = skill_meta.icon
        if element == Element.Passive:
            mp_cost.setText("MP cost: N/A")
        else:
            mp_cost.setText("MP cost: " + str(skill_meta.mp_cost))
        try:
            pak = ICON_LOADER.element_icon(element)
        except Exception as e:
            print_icon_loading_error(e, "Failed to load element icon:")
        else:
            pix = pak.pixmap.scaled(pak.size_div(2))
            icon.setFixedSize(pix.size())
            icon.setPixmap(pix)

    def make_meta_refresh_callback(
        self,
        icon: QLabel,
        mp_cost: QLabel,
    ):
        def inner(skill_id: int):
            return self.meta_refresh(skill_id, icon, mp_cost)
        return inner

    def stack_refresh(self):
        for i in range(9):
            skill_box, mystery_box = self.widgets[i]
            skill_box.refresh()
            skill = skill_box.skill
            mystery_box.setValue(skill._unknown)

    def on_apply_changes(self):
        for i in range(9):
            skill_box, mystery_box = self.widgets[i]
            skill_box.apply_changes()
            mystery_box.setattr_if_modified(skill_box.skill, "_unknown")
