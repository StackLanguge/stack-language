import collections
import pickle
import string
from constants import *

Token = collections.namedtuple('Token', 'TYPE VAL')


def split(s):
    s = s.strip()
    res = []
    in_string = False
    in_comment = False
    cur = []
    continue_more = 0
    for i, char in enumerate(s):
        if continue_more > 0:
            continue_more -= 1
            continue
        if i != len(s) - 1:
            chars = char + s[i + 1]
            if chars == COMMENT_START:
                in_comment = True
                continue_more = 1
                continue
            elif chars == COMMENT_END:
                in_comment = False
                continue_more = 1
                continue
            if in_comment:
                continue
        if char in string.whitespace and not in_string:
            w = ''.join(cur)
            if not w == '':
                res.append(w)
                cur = []
        else:
            if char == "/" and s[i+1] == "'":
                char = ''
            if char == "'":
                if i > 0 and s[i-1] == '/':
                    pass
                else:
                    in_string = not in_string
            cur.append(char)
    if cur:
        res.append(''.join(cur))
    return res


def _parse_iter(prog):
    prog_len = len(prog) - 1
    prog_index = -1
    tokens = []
    # in_comment = False
    while prog_index < prog_len:
        prog_index += 1
        tok = prog[prog_index]
        # if in_comment:
        #     if tok == COMMENT_END:
        #         in_comment = False
        # else:
        # if tok == COMMENT_START:
        #     in_comment = True
        if is_op(tok):
            tokens.append(Token(TYPE='op', VAL=tok))
        elif is_str(tok):
            tokens.append(Token(TYPE='str', VAL=tok[1:-1]))
        elif is_num(tok):
            tokens.append(Token(TYPE='num', VAL=float(tok)))
        elif is_bool(tok):
            tokens.append(Token(
                TYPE='bool', VAL=(True if tok == 'True' else False)))
        elif is_list(tok):
            tokens.append(Token(TYPE='list', VAL=[]))
        elif is_name(tok):
            tokens.append(Token(TYPE='name', VAL=tok[1:]))
        elif is_var(tok):
            tokens.append(Token(TYPE='var', VAL=tok))
        elif tok == BLOCK_START:
            code, end = _parse_iter(prog[prog_index+1:])
            prog_index += end + 1
            tokens.append(Token(TYPE='code', VAL=code))
        elif tok == BLOCK_END:
            break
    return tokens, prog_index


def parse(prog_string):
    return _parse_iter(split(prog_string))[0]


def compile_to_file(prog, filename):
    code = parse(prog)
    f = open(filename, 'wb')
    pickle.dump(code, f)
    f.close()

if __name__ == '__main__':
    print(parse('''"spam" 'ham' print print'''))
    print(parse("5 `n set n"))
    print(parse("'hello' /* this is a comment */ 'world'"))
