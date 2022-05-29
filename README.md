# Myers diff

This is an implementation of Myers diff algorithm, without the linear space refinment.

The algorithm therefore runs in O((N+M)D) in time and space, where:
* N is the size of the first element
* M is the size of the second element
* D is the number of differences

## Example

The `diff` method can take any two sequences of objects. The only requirement is that the objects have the equality operator (`==`) defined.

```python
from diff.myers import diff, EditType

# the diff method returns a list of edits that
# turns the first sequence into the second
for edit in diff([1, 2, 3], [2, 3, 4]):
    if edit.type == EditType.KEEP:
        print(f' {edit.data}')
    if edit.type == EditType.INSERT:
        print(f'+{edit.data}')
    if edit.type == EditType.DELETE:
        print(f'-{edit.data}')
```

Outputs:

```shell
-1
 2
 3
+4
```

## HTML generator

You can generate a pretty view of the diff using the `html` helper.

```python
from diff.html import create_html_diff

html = create_html_diff("ABCABBA", "CBABAC")
open("diff.html", "w").write(html)
```

Produces:

<pre><span style="background-color: #FFCDD2;">A</span><span style="background-color: #FFCDD2;">B</span>C<span style="background-color: #C8E6C9;">B</span>AB<span style="background-color: #FFCDD2;">B</span>A<span style="background-color: #C8E6C9;">C</span></pre>