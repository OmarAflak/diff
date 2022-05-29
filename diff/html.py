from typing import Iterable, TypeVar
from diff.myers import diff, EditType

T = TypeVar("T")

def create_html_diff(s1: Iterable[T], s2: Iterable[T], join: str = "") -> str:
    result = "<pre>"
    for e in diff(s1, s2):
        if e.type == EditType.KEEP:
            result += e.data
        if e.type == EditType.INSERT:
            result += f'<span style="background-color: #C8E6C9;">{e.data}</span>'
        if e.type == EditType.DELETE:
            result += f'<span style="background-color: #FFCDD2;">{e.data}</span>'
    result += "</pre>"
    return result