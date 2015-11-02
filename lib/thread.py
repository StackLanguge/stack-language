import threading


def tstart(interpeter, stack, scopes, stream):
    val = stack.pop()

    def func():
        stream.append(interpeter.Token(TYPE='code', VAL=val.VAL))
        stream.append(interpeter.Token(TYPE='op', VAL='call'))

    thread = threading.Thread(target=func)
    thread.start()


module = {
    "tstart": tstart
}
