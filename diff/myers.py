from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar
from enum import Enum

T = TypeVar("T")

class EditType(Enum):
    INSERT = 1
    DELETE = 2
    KEEP = 3

@dataclass
class Edit(Generic[T]):
    type: EditType
    data: T

def _diff(s1: Iterable[T], s2: Iterable[T]) -> list[tuple[int, int]]:
    furthest_x: dict[int, tuple[int, list]] = {1: (0, [])}
    M = len(s1)
    N = len(s2)

    for d in range(M + N + 1):
        for k in range(-d, d + 1, 2):
            down = (k == -d or (k != d and furthest_x[k + 1][0] > furthest_x[k - 1][0]))
            previous_k = k + 1 if down else k - 1

            x_start, history = furthest_x[previous_k]
            history = history[:]

            x_middle = x_start if down else x_start + 1
            y_middle = x_middle - k
            history.append((x_middle, y_middle))

            x_end = x_middle
            y_end = x_end - k
            while x_end < M and y_end < N and s1[x_end] == s2[y_end]:
                x_end += 1
                y_end += 1
                history.append((x_end, y_end))

            furthest_x[k] = (x_end, history)

            if x_end >= M and y_end >= N:
                return history

    assert False

def diff(s1: Iterable[T], s2: Iterable[T]) -> list[Edit[T]]:
    edit_script: list[Edit[T]] = []
    pairs = _diff(s1, s2)
    for i in range(1, len(pairs)):
        dx = pairs[i][0] - pairs[i - 1][0]
        dy = pairs[i][1] - pairs[i - 1][1]
        if dx == 1 and dy == 1:
            edit_script.append(Edit(EditType.KEEP, s1[pairs[i][0] - 1]))
        if dx == 1 and dy == 0:
            edit_script.append(Edit(EditType.DELETE, s1[pairs[i][0] - 1]))
        if dx == 0 and dy == 1:
            edit_script.append(Edit(EditType.INSERT, s2[pairs[i][1] - 1]))
    return edit_script