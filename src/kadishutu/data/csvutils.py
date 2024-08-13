from abc import ABC
import csv
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypeVar
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
                except:
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
                    value = item[k_info["field_name"]]
                except KeyError:
                    value = item[k]
                try:
                    value = k_info["converter"](v, value)
                except:
                    value = v(value)
                target_item[k] = value
            res.append(target_item)
        return [
            cls(**i)
            for i in res
        ]


def is_unused(name: str) -> bool:
    return name.startswith("NOT USED:")


class IHaveAName(ABC):
    name: str

    def is_unused(self) -> bool:
        return is_unused(self.name)


T = TypeVar("T")


def make_maps(objs: List[T]) -> Tuple[Dict[int, T], Dict[str, T]]:
    id_to_name_map = {}
    name_to_id_map = {}
    for obj in objs:
        id_to_name_map[obj.id] = obj  # type: ignore
        name_to_id_map[obj.name] = obj  # type: ignore
    return (id_to_name_map, name_to_id_map)


def make_maps_dict(objs: List[T]) -> Tuple[Dict[int, T], Dict[str, T]]:
    id_to_name_map = {}
    name_to_id_map = {}
    for obj in objs:
        id_to_name_map[obj["id"]] = obj  # type: ignore
        name_to_id_map[obj["name"]] = obj  # type: ignore
    return (id_to_name_map, name_to_id_map)
