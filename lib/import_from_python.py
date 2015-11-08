import importlib
import inspect
import types


def import_from_python(interpeter, stack, scopes, stream):
    val = stack.pop()
    mod = importlib.import_module(val.VAL)
    tok = interpeter.Token(TYPE="py-obj", VAL=mod)
    stack.append(tok)


def py_call(interpeter, stack, scopes, stream):
    val2, val = stack.pop(), stack.pop()

    if not val.TYPE == "py-obj":
        interpeter.report_error(
            "TYPE",
            "py_call",
            "%s is not a py-obj!" % val)
    if not isinstance(val.VAL, types.FunctionType):
        interpeter.report_error(
            "TYPE",
            "py_call",
            "%s.VAL is not a Python function!")

    f = val.VAL

    spec = inspect.getargspec(f)

    defaults = zip(reversed(spec.args), reversed(spec.defaults))
    kwargs = dict(defaults)

    args = []
    for arg in val2.VAL:
        args.append(arg)

    # print("KW-ARGS:", kwargs)
    # print("ARGS:", args)
    # print("FUNC:", f)

    res = f(*args, **kwargs)

    # print("RES:", repr(res))

    tok = interpeter.Token(TYPE="py-obj", VAL=res)
    stack.append(tok)


module = {
    "import_from_python": import_from_python,
    "py_call": py_call
}
