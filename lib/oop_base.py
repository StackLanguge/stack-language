import types


def mapobj(interpeter, stack, scopes, stream):
    val1 = stack.pop()
    obj = {}
    for item in val1.VAL:
        key = item.VAL[0].VAL
        val = item.VAL[1].VAL
        obj[key] = val
    tok = interpeter.Token(TYPE="py-obj", VAL=obj)
    stack.append(tok)


def newobj(interpeter, stack, scopes, stream):
    tok = interpeter.Token(TYPE="py-obj", VAL={})
    stack.append(tok)


def prop(interpeter, stack, scopes, stream):
    val2, val1 = stack.pop().VAL, stack.pop().VAL

    if isinstance(val2, dict):
        if not val2 in val1.keys():
            interpeter.report_error(
                "OOP_ERROR",
                "propof",
                "Property not in object!")
    elif "__all__" in dir(val2):
        if not val2 in val1.__all__:
            interpeter.report_error(
                "OOP_ERROR",
                "propof",
                "Property not in object!")
    elif not val2 in dir(val1):
        interpeter.report_error(
            "OOP_ERROR",
            "propof",
            "Property not in object!")

    if isinstance(val1, types.ModuleType):
        value = val1.__dict__[val2]
    else:
        value = val1[val2]

    tok = interpeter.Token(TYPE='py-obj', VAL=value)
    stack.append(tok)


def setprop(interpeter, stack, scopes, stream):
    val3, val2, val1 = [i.VAL for i in (stack.pop(), stack.pop(), stack.pop())]
    val1[val2] = val3
    stack.append(val1)


module = {
    "newobj": newobj,
    "mapobj": mapobj,
    "prop": prop,
    "setprop": setprop
}
