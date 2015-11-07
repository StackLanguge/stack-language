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


def _propof(val1, val2, interpeter):
    if not val1 in val2.keys():
        interpeter.report_error(
            "OOP_ERROR",
            "propof",
            "Property not in object!")
    value = val2[val1]
    return value


def arrow_setprop(interpeter, stack, scopes, stream):
    val3, val2, val1 = [i.VAL for i in (stack.pop(), stack.pop(), stack.pop())]
    val1[val2] = val3


def propof(interpeter, stack, scopes, stream):
    val2, val1 = stack.pop().VAL, stack.pop().VAL
    value = _propof(val1, val2, interpeter)
    tok = interpeter.Token(TYPE='py-obj', VAL=value)
    stack.append(tok)


def arrow_propof(interpeter, stack, scopes, stream):
    val2, val1 = stack.pop().VAL, stack.pop().VAL
    value = _propof(val2, val1, interpeter)
    tok = interpeter.Token(TYPE='py-obj', VAL=value)
    stack.append(tok)


module = {
    "newobj": newobj,
    "mapobj": mapobj,
    "propof": propof,
    "->": arrow_propof,
    "<-": arrow_setprop
}
