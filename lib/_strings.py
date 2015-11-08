def _len(interpeter, stack, scopes, stream):
    val = stack.pop()
    tok = interpeter.Token(
        TYPE='num', VAL=len(val.VAL))
    stack.append(tok)

module = {
    "_len": _len
}
