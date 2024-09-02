from typing import Iterable, TypeVar
from diff.myers import diff, Operation

T = TypeVar('T')

def create_html_diff(s1: Iterable[T], s2: Iterable[T], break_line: bool = False) -> str:
    html = ''.join(
        _format_data(data, edit.operation, break_line)
        for edit in diff(s1, s2)
        for data in edit.data
    )
    return f'<pre>{html}</pre>'

def _format_data(data: T, operation: Operation, break_line: bool) -> str:
    br = '</br>' if break_line else ''
    if operation == Operation.KEEP:
        return data + br
    if operation == Operation.INSERT:
        return f'<span style="background-color: #C8E6C9;">{data}</span>{br}'
    if operation == Operation.DELETE:
        return f'<span style="background-color: #FFCDD2;">{data}</span>{br}'
