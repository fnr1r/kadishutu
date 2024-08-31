from abc import ABC
import csv
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
import re
from typing import (
    Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple, Type,
    TypeVar,
)
from typing_extensions import Self


FILE_PATH = Path(os.path.realpath(__file__)).parent
TABLES_PATH = FILE_PATH / "tables"


def csvread_headerless(path: Path, skip_lines: int = 0) -> List[List[str]]:
    with open(path, "rt") as file:
        while skip_lines > 0:
            if file.read(1) == "\n":
                skip_lines -= 1
        return [
            i
            for i in csv.reader(file)
        ]


def csvread(path: Path, skip_lines: int = 0) -> List[Dict[str, str]]:
    with open(path, "rt") as file:
        while skip_lines > 0:
            if file.read(1) == "\n":
                skip_lines -= 1
        return [
            i
            for i in csv.DictReader(file)
        ]


@dataclass
class FromCsv:
    @classmethod
    def filter_data(cls, item: Dict[str, str]) -> bool:
        return True

    @classmethod
    def converter_data(cls) -> Optional[Dict[str, Dict[str, Any]]]:
        ...

    @classmethod
    def from_csv_headerless(cls, path: Path, skip_lines: int = 0) -> List[Self]:
        csv_data = csvread_headerless(path, skip_lines)
        res = []
        conversion_info = cls.converter_data()
        for item in csv_data:
            target_item = []
            for i, (k, v) in enumerate(cls.__annotations__.items()):
                if not conversion_info:
                    k_info = {}
                else:
                    try:
                        k_info = conversion_info[k]
                    except KeyError:
                        k_info = {}
                value = item[i]
                try:
                    value = k_info["converter"](v, value)
                except KeyError:
                    value = v(value)
                target_item.append(value)
            res.append(target_item)
        return [
            cls(*i)
            for i in res
        ]

    @classmethod
    def from_csv(cls, path: Path, skip_lines: int = 0) -> List[Self]:
        csv_data = csvread(path, skip_lines)
        res = []
        conversion_info = cls.converter_data()
        for item in csv_data:
            if not cls.filter_data(item):
                continue
            target_item = {}
            for k, v in cls.__annotations__.items():
                if not conversion_info:
                    k_info = {}
                else:
                    try:
                        k_info = conversion_info[k]
                    except KeyError:
                        k_info = {}
                try:
                    fun: Callable[[Dict[str, str]], Any] = k_info["eval"]
                except KeyError:
                    pass
                else:
                    value = fun(item)
                    target_item[k] = value
                    continue
                try:
                    value = item[k_info["field_name"]]
                except KeyError:
                    value = item[k]
                try:
                    value = k_info["converter"](v, value)
                except KeyError:
                    value = v(value)
                target_item[k] = value
            res.append(target_item)
        return [
            cls(**i)
            for i in res
        ]


EXTRACTOR_RE = re.compile(r"(\d+) \((.+)\)")


def extractor(text: str) -> Tuple[int, str]:
    res = EXTRACTOR_RE.match(text)
    assert res
    g = res.groups()
    return (int(g[0]), g[1])


REVERSE_EXTRACTOR_RE = re.compile(r"(.+) \((\d+)\)")


def reverse_extractor(text: str) -> Tuple[str, int]:
    res = REVERSE_EXTRACTOR_RE.match(text)
    assert res
    g = res.groups()
    return (g[0], int(g[1]))


T = TypeVar("T", bound=Enum)


def extract_from_str(cls: Type[T], text: str) -> T:
    (num, _) = extractor(text)
    return cls(num)


def is_unused(name: str) -> bool:
    return name.startswith("NOT USED:")


class IHaveAName(ABC):
    name: str

    def is_unused(self) -> bool:
        return is_unused(self.name)


class RandType(Protocol):
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, v: str): ...


T = TypeVar("T", bound=RandType)


def make_maps(objs: Sequence[T]) -> Tuple[Dict[int, T], Dict[str, T]]:
    id_to_name_map: Dict[int, Any] = {}
    name_to_id_map: Dict[str, Any] = {}
    for obj in objs:
        id_to_name_map[obj.id] = obj
        if obj.name in name_to_id_map.keys():
            new_name = f"{obj.name} ({obj.id})"
            name_to_id_map[new_name] = obj
            obj.name = new_name
        else:
            name_to_id_map[obj.name] = obj
    return (id_to_name_map, name_to_id_map)
