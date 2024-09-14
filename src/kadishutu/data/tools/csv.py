import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from typing import (
    Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar,
)
from typing_extensions import Self


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
    def from_csv_headerless(
        cls,
        path: Path,
        skip_lines: int = 0
    ) -> List[Self]:
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
