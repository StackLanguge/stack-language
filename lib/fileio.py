import os.path


def fopen(interpeter, stack, scopes, stream):
    val = stack.pop()
    tok = interpeter.Token(TYPE="py-obj", VAL={
        "path": os.path.abspath(val.VAL)
    })
    stack.append(tok)


def fread(interpeter, stack, scopes, stream):
    val = stack.pop()
    with open(val.VAL["path"], "r") as f:
        tok = interpeter.Token(TYPE="str", VAL=f.read())
        stack.append(tok)


module = {
    "fopen": fopen,
    "fread": fread
}
