from typing import List, Tuple, TypeVar


T = TypeVar('T')


def group_objects(
    objects: List[T],
    group_size: int,
    allow_partial: bool = False
) -> List[Tuple[T, ...]]:
    if group_size <= 0:
        raise ValueError("group_size must be a positive integer")
    if not allow_partial and len(objects) % group_size != 0:
        raise ValueError("bad group size")
    
    res = []
    for i in range(0, len(objects), group_size):
        group = tuple(objects[i:i+group_size])
        if len(group) != group_size:
            if not group:
                continue
            if not allow_partial:
                raise ValueError("bad group size")
        res.append(group)
    
    return res
