import sys
import time
import stack_parser
import os
from constants import *


class Token:
    def __init__(self, TYPE, VAL):
        self.TYPE = TYPE
        self.VAL = VAL

    def __str__(self):
        return 'Token(TYPE=%s, VAL=%s)' % (str(self.TYPE), str(self.VAL))


def report_error(error_type, op, error_msg):
    print('***%s ERROR***' % error_type)
    print('Operation: %s' % op)
    print(error_msg)
    sys.exit(1)


def _stream_interpet(token_stream):
    scopes = [{'user-words': {}}]
    data_stack = []
    #print(token_stream)
    for i, token in enumerate(token_stream):
        #print(i, token)
        if token.TYPE in DATA_TYPES:
            #Push data onto the stack
            data_stack.append(token)
        elif token.TYPE == 'var':
            #Token is the name of a var or user defined word
            # Retrieve the var or call the word
            if 'var_' + token.VAL in scopes[-1]:
                token_stream[i+1:i+1] = [
                    Token(TYPE='name', VAL=token.VAL),
                    Token(TYPE='op', VAL='get')
                ]
            elif 'word_' + token.VAL in scopes[-1]['user-words']:
                token_stream[i+1:i+1] = [
                    Token(TYPE='name', VAL=token.VAL),
                    Token(TYPE='op', VAL='call')
                ]
            else:
                print(scopes)
                report_error(
                    'DATA_ERROR',
                    '~intrnal',
                    '%s is not defined as a variable or word!' % token.VAL)
        else:
            #Token is a word

            #INDEX:
            # (op type)   (lines)
            # Math ops: 32-149
            # String ops: 150-173
            # IO ops: 174-191
            # Data Stack ops: 193-212
            # Bool ops: 214-269
            # List ops: 272-445
            # Scope and variable ops: 446-499
            # Misc ops: 500-512
            # Control Flow ops: 514-549
            # User words ops: 550-578

            op = token.VAL
            #Math ops
            if op == '+':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '+',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', '+',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', '+',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=val1.VAL+val2.VAL)
                data_stack.append(res)
            elif op == '-':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '-',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', '-',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', '-',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=val1.VAL-val2.VAL)
                data_stack.append(res)
            elif op == '*':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '*',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', '*',
                                 ' %s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', '*',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=val1.VAL*val2.VAL)
                data_stack.append(res)
            elif op == '/':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '/',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', '/',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', '/',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=val1.VAL/val2.VAL)
                data_stack.append(res)
            elif op == 'num':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'num',
                                 'There are not enough values to pop.')
                res = Token(TYPE='num', VAL=float(val1.VAL))
                data_stack.append(res)
            elif op == 'BAND':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'BAND',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', 'BAND',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'BAND',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=int(val1.VAL) & int(val2.VAL))
                data_stack.append(res)
            elif op == 'BOR':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'BOR',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', 'BOR',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'BOR',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=int(val1.VAL) | int(val2.VAL))
                data_stack.append(res)
            elif op == 'BXOR':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'BXOR',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', 'BXOR',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'BXOR',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=int(val1.VAL) ^ int(val2.VAL))
                data_stack.append(res)
            elif op == 'BNOT':
                try:
                    val2 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'BNOT',
                                 'There are not enough values to pop.')
                if val2.TYPE != 'num':
                    report_error('TYPE', 'BNOT',
                                 '%s is not a number!' % str(val2))
                res = Token(TYPE='num', VAL=~int(val2.VAL))
                data_stack.append(res)
            #String ops
            elif op == 'concat':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'concat',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'str':
                    report_error('TYPE', 'concat',
                                 '%s is not a string!' % str(val1))
                if val2.TYPE != 'str':
                    report_error('TYPE', 'concat',
                                 '%s is not a string!' % str(val2))
                res = Token(TYPE='str', VAL=val1.VAL+val2.VAL)
                data_stack.append(res)
            elif op == 'string':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'string',
                                 'There are not enough values to pop.')
                res = Token(TYPE='str', VAL=str(val1.VAL))
                data_stack.append(res)
            elif op == 'letterof':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'letterof',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', 'letterof',
                                 '%s is not a number!' % str(val1))
                if val2.TYPE != 'str':
                    report_error('TYPE', 'letterof',
                                 '%s is not a string!' % str(val2))
                res = Token(TYPE='str', VAL=val2.VAL[val1.VAL])
                data_stack.append(res)
            #IO ops
            elif op == 'print':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'string',
                                 'There are not enough values to pop.')
                print(val.VAL)
            elif op == 'input':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'input',
                                 'There are not enough values to pop.')
                res = input(val.VAL)
                res = Token(TYPE='str', VAL=res)
                data_stack.append(res)
            #Data stack ops
            elif op == 'pop':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'pop',
                                 'There are not enough values to pop.')
            elif op == 'dup':
                try:
                    res = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'pop',
                                 'There are not enough values to pop.')
                data_stack.append(res)
                data_stack.append(res)

            elif op == 'dumpstack':
                print('***DATA STACK DUMP***')
                for i, tok in enumerate(data_stack):
                    print('Item %s: %s' % (i, tok))
            #Bool ops
            elif op == 'or':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'or',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'bool':
                    report_error('TYPE', 'or',
                                 '%s is not a bool!' % str(val1))
                if val2.TYPE != 'bool':
                    report_error('TYPE', 'or',
                                 '%s is not a bool!' % str(val2))
                res = Token(TYPE='bool', VAL=(val1.VAL or val2.VAL))
                data_stack.append(res)
            elif op == 'and':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'and',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'bool':
                    report_error('TYPE', 'and',
                                 '%s is not a bool!' % str(val1))
                if val2.TYPE != 'bool':
                    report_error('TYPE', 'and',
                                 '%s is not a bool!' % str(val2))
                res = Token(TYPE='bool', VAL=(val1.VAL and val2.VAL))
                data_stack.append(res)
            elif op == 'not':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'not',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'bool':
                    report_error('TYPE', 'not',
                                 '%s is not a bool!' % str(val1))
                res = Token(TYPE='bool', VAL=(not val1.VAL))
                data_stack.append(res)
            elif op == '=':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '=',
                                 'There are not enough values to pop.')
                res = Token(
                    TYPE='bool',
                    VAL=((val1.TYPE == val2.TYPE) and (val1.VAL == val2.VAL)))
                data_stack.append(res)
            elif op == '!=':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', '!!=',
                                 'There are not enough values to pop.')
                res = Token(
                    TYPE='bool',
                    VAL=((val1.TYPE != val2.TYPE) or (val1.VAL != val2.VAL)))
                data_stack.append(res)
            #List ops
            elif op == 'lnth':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lnth',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lnth',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'lnth',
                                 '%s is not a number!' % str(val2))
                data_stack.append(val1.VAL[int(val2.VAL)])
            elif op == 'lappend':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lappend',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lappend',
                                 '%s is not a list!' % str(val1))
                val1.VAL.append(val2)
                data_stack.append(val1)
            elif op == 'llen':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'llen',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'llen',
                                 '%s is not a list!' % str(val1))
                data_stack.append(Token(TYPE='num', VAL=len(val1.VAL)))
            elif op == 'lslice':
                try:
                    val3, val2, val1 = (
                        data_stack.pop(), data_stack.pop(), data_stack.pop())
                except IndexError:
                    report_error('DATA_STACK', 'lslice',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lslice',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'lslice',
                                 '%s is not a number!' % str(val2))
                if val3.TYPE != 'num':
                    report_error('TYPE', 'lslice',
                                 '%s is not a number!' % str(val3))
                data_stack.append(Token(
                    TYPE='list',
                    VAL=val1.VAL[int(val2.VAL):int(val3.VAL)]))
            elif op == 'lin':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lin',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lin',
                                 '%s is not a list!' % str(val1))
                data_stack.append(Token(TYPE='bool', VAL=val2 in val1.VAL))
            elif op == 'linsert':
                try:
                    val3, val2, val1 = (
                        data_stack.pop(), data_stack.pop(), data_stack.pop())
                except IndexError:
                    report_error('DATA_STACK', 'linsert',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'linsert',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'linsert',
                                 '%s is not a number!' % str(val2))
                val1.VAL.insert(int(val3.VAL), val2)
                data_stack.append(val1)
            elif op == 'lindex':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lindex',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lindex',
                                 '%s is not a list!' % str(val1))
                try:
                    n = val1.VAL.index(val2)
                except ValueError:
                    n = -1
                data_stack.append(Token(TYPE='num', VAL=n))
            elif op == 'lreverse':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lreverse',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lreverse',
                                 '%s is not a list!' % str(val1))
                val1.VAL.reverse()
                data_stack.append(val1)
            elif op == 'lclear':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lclear',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lclear',
                                 '%s is not a list!' % str(val1))
                val1.VAL.clear()
                data_stack.append(val1)
            elif op == 'lpop':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lpop',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lpop',
                                 '%s is not a list!' % str(val1))
                try:
                    v = val1.VAL.pop()
                except IndexError:
                    report_error('LIST_ERROR', 'lpop',
                                 'List is empty!')
                else:
                    data_stack.append(v)
            elif op == 'lpopn':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'lpopn',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lpopn',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'lpopn',
                                 '%s is not a number!' % str(val2))
                try:
                    v = val1.VAL.pop(int(val2.VAL))
                except IndexError:
                    report_error('LIST_ERROR', 'lpopn',
                                 'List is empty!')
                else:
                    data_stack.append(v)
            elif op == 'ldeln':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'ldeln',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'ldeln',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'ldeln',
                                 '%s is not a number!' % str(val2))
                del val1.VAL[int(val2.VAL)]
                data_stack.append(val1)
            elif op == 'lreplace':
                try:
                    val3, val2, val1 = (
                        data_stack.pop(), data_stack.pop(), data_stack.pop())
                except IndexError:
                    report_error('DATA_STACK', 'lreplace',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'list':
                    report_error('TYPE', 'lreplace',
                                 '%s is not a list!' % str(val1))
                if val2.TYPE != 'num':
                    report_error('TYPE', 'lreplace',
                                 '%s is not a number!' % str(val2))
                val1.VAL[int(val2.VAL)] = val3
                data_stack.append(val1)
            #Scope and variable ops
            elif op == 'push_scope':
                scopes.append({'user-words': {}})
            elif op == 'dump_scope':
                print(scopes)
            elif op == 'pop_scope':
                if len(scopes) < 2:
                    report_error('SCOPE_UNDERFLOW', 'pop_scope',
                                 'You can not pop the global scope!')
                else:
                    scopes.pop()
            elif op == 'set':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'set',
                                 'There are not enough values to pop.')
                if val2.TYPE != 'name':
                    report_error('TYPE', 'set',
                                 '%s is not a name!' % str(val2))
                else:
                    scopes[-1]['var_' + val2.VAL] = val1
            elif op == 'get':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'get',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'name':
                    report_error('TYPE', 'get',
                                 '%s is not a name!' % str(val1))
                #Find the var
                for i in range(len(scopes) - 1, -1, -1):
                    if ('var_' + val1.VAL) in scopes[i]:
                        data_stack.append(scopes[i]['var_' + val1.VAL])
                        break
                else:
                    report_error('VARAIBLE_ERROR', 'get',
                                 'The variable %s does not exist!' % val1.VAL)
            elif op == 'del':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'del',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'name':
                    report_error('TYPE', 'del',
                                 '%s is not a name!' % str(val1))
                try:
                    del scopes[-1]['var_' + val1.VAL]
                except KeyError:
                    report_error('VARAIBLE_ERROR', 'del',
                                 '%s is not a variable!' % val1.VAL)
            #Misc ops
            elif op == 'wait':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'wait',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'num':
                    report_error('TYPE', 'wait',
                                 '%s is not a number!' % str(val1))
                time.sleep(val1.VAL)

            elif op == 'reverse':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'reverse',
                                 'There are not enough values to pop.')
                if val1.TYPE not in ('list', 'str'):
                    report_error('TYPE', 'reverse',
                                 '%s is not a string or a list!' % str(val1))
                res = Token(TYPE=val1.TYPE, VAL=val1.VAL[::-1])
                data_stack.append(res)
            #Control flow ops
            elif op == 'if':
                try:
                    val1, val2 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'if',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'code':
                    report_error('TYPE', 'if',
                                 '%s is not a code block!' % str(val1))
                if val2.TYPE != 'bool':
                    report_error('TYPE', 'if',
                                 '%s is not a bool!' % str(val1))
                if val2.VAL:
                    token_stream[i+1:i+1] = val1.VAL

            elif op == 'ifelse':
                try:
                    val1, val2, val3 = (
                        data_stack.pop(), data_stack.pop(), data_stack.pop())
                except IndexError:
                    report_error('DATA_STACK', 'ifelse',
                                 'There are not enough values to pop.')
                #print(val3,val2,val1)
                if val1.TYPE != 'code':
                    report_error('TYPE', 'ifelse',
                                 '%s is not a code block!' % str(val1))
                if val2.TYPE != 'code':
                    report_error('TYPE', 'ifelse',
                                 '%s is not a code block!' % str(val1))
                if val3.TYPE != 'bool':
                    report_error('TYPE', 'ifelse',
                                 '%s is not a bool!' % str(val1))
                if val3.VAL:
                    token_stream[i+1:i+1] = val2.VAL
                else:
                    token_stream[i+1:i+1] = val1.VAL

            #User word ops
            elif op == 'def':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'def',
                                 'There are not enough values to pop.')
                if val1.TYPE != 'code':
                    report_error('TYPE', 'def',
                                 '%s is not a code block!' % str(val1))
                if val2.TYPE != 'name':
                    report_error('TYPE', 'def',
                                 '%s is not a name!' % str(val1))
                scopes[-1]['user-words']['word_' + val2.VAL] = val1
            elif op == 'call':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'call',
                                 'There are not enough values to pop.')
                if val1.TYPE == 'code':
                    token_stream[i+1:i+1] = val1.VAL
                elif (
                    val1.TYPE == 'name' and
                    'word_' + val1.VAL in scopes[-1]['user-words']
                ):
                    token_stream[i+1:i+1] = (
                        scopes[-1]['user-words']['word_' + val1.VAL].VAL)
                else:
                    report_error('WORD_ERROR', 'call',
                                 '%s is not a callable object!' % str(val1))
            elif op == 'import':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error('DATA_STACK', 'call',
                                 'There are not enough values to pop.')
                file_path = os.path.abspath(val1.VAL) + ".stack"
                f = open(file_path, "r")
                f_data = f.read()
                f.close()
                tok_stream, result_scopes = interpet(f_data)
                for tok in tok_stream:
                    data_stack.append(tok)
                for scope in result_scopes:
                    scopes.append(scope)
    return data_stack, scopes


def interpet(prog):
    tok_stream = stack_parser.parse(prog)
    return _stream_interpet(tok_stream)
