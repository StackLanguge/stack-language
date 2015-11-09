import os.path


def fopen(interpeter, stack, scopes, stream):
    '''

        Pushes a py-obj onto the stack with some data about the
        file trying to be accessed (i.e. its path).

        Syntax:
            <str> fopen

        Examples:
            'read.txt' fopen print -> {'path': '.../read.txt'}

    '''

    val = stack.pop()
    tok = interpeter.Token(TYPE="py-obj", VAL={
        "path": os.path.abspath(val.VAL)
    })
    stack.append(tok)


def fread(interpeter, stack, scopes, stream):
    '''

        Pushes a string onto the stack with the contents of
        the path of the given py-obj.

        Syntax:
            <py-obj> fread

        Examples:
            'read.txt' fopen fread print -> [contents here]

    '''

    val = stack.pop()
    with open(val.VAL["path"], "r") as f:
        tok = interpeter.Token(TYPE="str", VAL=f.read())
        stack.append(tok)


def freadnobreak(interpeter, stack, scopes, stream):
    '''

        Like fread, but strips a SINGLE newline (if available)
        off of the contents of the file read.

        Syntax:
            <py-obj> freadnobreak

        Examples:
            'read_with_newline.txt' fopen fread print -> [contents (newline)]
            'read_with_newline.txt' fopen freadnobreak -> [contents]

    '''

    val = stack.pop()
    with open(val.VAL["path"], "r") as f:
        data = f.read()
        if data[-1] == "\n":
            data = "\n".join(data.split("\n")[:-1])
        tok = interpeter.Token(TYPE="str", VAL=data)
        stack.append(tok)


def fwrite(interpeter, stack, scopes, stream):
    '''

        Writes text to a file from the given py-obj's path property.

        Syntax:
            <py-obj> <str> fwrite

        Examples:
            'write.txt' fopen dup 'Hello!' fwrite fread print -> Hello!

    '''

    val2, val1 = stack.pop(), stack.pop()
    with open(val1.VAL["path"], "w+") as f:
        f.write(val2.VAL)


def fwritebreak(interpeter, stack, scopes, stream):
    '''

        Like fwrite, but appends a line break to the end of the
        data written.

        Syntax:
            <py-obj> <str> fwritebreak

        Examples:
            'write_with_newline.txt' fopen dup 'Hey you!' fwritebreak
            fread print -> Hey you!(newline)

    '''

    val2, val1 = stack.pop(), stack.pop()
    data = "\n".join(val2.VAL.split("\n")) + "\n"
    with open(val1.VAL["path"], "w+") as f:
        f.write(data)


module = {
    "fopen": fopen,
    "fread": fread,
    "freadnobreak": freadnobreak,
    "fwrite": fwrite,
    "fwritebreak": fwritebreak
}
