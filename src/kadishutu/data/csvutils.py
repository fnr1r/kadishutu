from abc import ABC
from typing import Dict, List, Optional, Tuple, TypeVar
from typing_extensions import Self
from pandas import DataFrame, read_csv
from pathlib import Path

class PandasMixin(ABC):
    @classmethod
    def from_dataframe(
        cls, df: DataFrame, rename: Optional[Dict[str, str]] = None
    ) -> list[Self]:
        if rename:
            df = df.rename(columns=rename)
        return [
            cls(**row)
            for row in df[list(cls.__annotations__.keys())].to_dict(orient="records")
        ]
    @classmethod
    def from_csv(
        cls, path: Path, *args, skiprows: Optional[int] = None, **kwargs
    ) -> list[Self]:
        with open(path, "r") as file:
            if skiprows:
                df = read_csv(file, skiprows=skiprows)
            else:
                df = read_csv(file)
        return cls.from_dataframe(df, *args, **kwargs)


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
