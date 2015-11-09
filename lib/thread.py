'''
    Threading for Stack

    This is very incomplete and SHOULD NOT BE USED.
'''

import copy
import threading


def tstart(interpeter, stack, scopes, stream):
    val = stack.pop()

    def func():
        # print(stream)
        new_stream = []
        for i in scopes:
            print("--", i)
            for j in i:
                print("-- --", i)
        new_stream.append(interpeter.Token(TYPE='code', VAL=val.VAL))
        new_stream.append(interpeter.Token(TYPE='op', VAL='call'))
        interpeter._stream_interpet(
            new_stream, location=scopes[-1]["var___file__"].VAL)

    thread = threading.Thread(target=func)
    thread.start()


module = {
    "tstart": tstart
}
