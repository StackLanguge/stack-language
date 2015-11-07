import importlib


def import_from_python(interpeter, stack, scopes, stream):
    val = stack.pop()
    mod = importlib.import_module(val.VAL)
    tok = interpeter.Token(TYPE="py-obj", VAL=mod)
    stack.append(tok)


module = {
    "import_from_python": import_from_python
}
