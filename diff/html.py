from typing import Iterable, TypeVar
from diff.myers import diff, Operation

T = TypeVar("T")

def _format_data(data: T, operation: Operation) -> str:
    if operation == Operation.KEEP:
        return data
    if operation == Operation.INSERT:
        return f'<span style="background-color: #C8E6C9;">{data}</span>'
    if operation == Operation.DELETE:
        return f'<span style="background-color: #FFCDD2;">{data}</span>'
    raise RuntimeError(f'Did not recognize operation {operation}')

def create_html_diff(s1: Iterable[T], s2: Iterable[T]) -> str:
    result = '<pre>'
    for edit in diff(s1, s2):
        for data in edit.data:
            result += _format_data(data, edit.operation)
    result += '</pre>'
    return result