from cgitb import html
from typing import Iterable, TypeVar
from diff.myers import diff, Operation

T = TypeVar('T')

def create_html_diff(s1: Iterable[T], s2: Iterable[T]) -> str:
    html = ''.join(
        _format_data(data, edit.operation)
        for edit in diff(s1, s2)
        for data in edit.data
    )
    return f'<pre>{html}</pre>'

def _format_data(data: T, operation: Operation) -> str:
    if operation == Operation.KEEP:
        return data
    if operation == Operation.INSERT:
        return f'<span style="background-color: #C8E6C9;">{data}</span>'
    if operation == Operation.DELETE:
        return f'<span style="background-color: #FFCDD2;">{data}</span>'
    raise RuntimeError(f'Did not recognize operation {operation}')