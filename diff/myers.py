from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar, Optional
from enum import Enum

T = TypeVar("T")

class Operation(Enum):
    INSERT = 1
    DELETE = 2
    KEEP = 3

@dataclass
class Edit(Generic[T]):
    operation: Operation
    data: list[T]

def diff(s1: Iterable[T], s2: Iterable[T]) -> list[Edit[T]]:
    tail = _diff(s1, s2)
    print(tail)
    head = tail.reverse()

    previous = head.previous
    current = previous.previous

    edit_script: list[Edit[T]] = []

    while current:
        dx = current.x - previous.x
        dy = current.y - previous.y

        if dx == 1 and dy == 1:
            edit = Edit(Operation.KEEP, [s1[current.x - 1]])
        elif dx == 1 and dy == 0:
            edit = Edit(Operation.DELETE, [s1[current.x - 1]])
        elif dx == 0 and dy == 1:
            edit = Edit(Operation.INSERT, [s2[current.y - 1]])
        else:
            raise RuntimeError("Error while parsing diff")

        if not edit_script or edit_script[-1].operation != edit.operation:
            edit_script.append(edit)
        else:
            edit_script[-1].data.extend(edit.data)

        previous = current
        current = current.previous

    return edit_script

@dataclass
class _Point:
    x: int
    y: int
    previous: Optional['_Point'] = None

    def reverse(self) -> '_Point':
        _next: Optional[_Point] = None
        current = self
        while current:
            prev = current.previous
            current.previous = _next
            _next = current
            current = prev
        return _next
        


def _diff(s1: Iterable[T], s2: Iterable[T]) -> _Point:
    path: dict[int, _Point] = {1: _Point(0, 0)}
    M = len(s1)
    N = len(s2)

    for d in range(M + N + 1):
        for k in range(-d, d + 1, 2):
            down = (k == -d or (k != d and path[k + 1].x > path[k - 1].x))
            previous_k = k + 1 if down else k - 1

            last_point = path[previous_k]

            x_end = last_point.x if down else last_point.x + 1
            y_end = x_end - k
            end_point = _Point(x_end, y_end, last_point)

            while x_end < M and y_end < N and s1[x_end] == s2[y_end]:
                x_end += 1
                y_end += 1
                end_point = _Point(x_end, y_end, end_point)

            path[k] = end_point

            if x_end >= M and y_end >= N:
                return end_point

    raise RuntimeError("Error while diffing")