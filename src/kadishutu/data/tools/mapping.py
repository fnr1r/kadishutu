from typing import Any, Dict, Protocol, Sequence, Tuple, TypeVar


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
