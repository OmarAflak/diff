from diff.myers import diff, Operation

# the diff method returns a list of edits that
# turns the first sequence into the second
for edit in diff("abc", "eag"):
    if edit.operation == Operation.KEEP:
        print(f' {edit.data}')
    if edit.operation == Operation.INSERT:
        print(f'+{edit.data}')
    if edit.operation == Operation.DELETE:
        print(f'-{edit.data}')