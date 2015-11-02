BUILTIN_OPS = (
    #Math ops
    '+',
    '-',
    '*',
    '/',
    'num',
    'BAND',
    'BOR',
    'BXOR',
    'BNOT',
    #String ops
    'concat',
    'string',
    'letterof',
    #IO ops
    'print',
    'input',
    #Stack ops
    'pop',
    'dup',
    'dumpstack',
    #Bool ops
    'or',
    'and',
    '=',
    '!=',
    'not',
    #List ops
    'lnth',
    'lappend',
    'lslice',
    'llen',
    'lin',
    'linsert',
    'lindex',
    'lreverse',
    'lclear',
    'lpop',
    'lpopn',
    'ldeln',
    'lreplace',
    #Variable ops
    'set',
    'get',
    'del',
    #Control flow
    #'while',
    'if',
    'ifelse',
    #Word Definition ops
    'def',
    'call',
    #Scope ops
    'push_scope',
    'pop_scope',
    'dump_scope',
    #Misc ops
    'wait',
    'reverse',
    #Import ops
    'import',
)

DATA_TYPES = (
    'str',
    'num',
    'bool',
    'list',
    'name',
    'code',
    'py-obj'
)
BLOCK_START = '{'
BLOCK_END = '}'
BLOCKS = (BLOCK_START, BLOCK_END)

LIST_START = '['
LIST_END = ']'
LISTS = (LIST_START, LIST_END)

COMMENT_START = "/*"
COMMENT_END = "*/"
COMMENTS = (COMMENT_START, COMMENT_END)


def is_op(op):
    return op in BUILTIN_OPS


def is_str(val):
    try:
        return val[0] == "'" and val[-1] == "'"
    except (IndexError, TypeError):
        return False


def is_num(val):
    try:
        return type(float(val)) == float
    except ValueError:
        return False


def is_bool(val):
    return val in ('True', 'False')


def is_list(val):
    return val in ('[]', 'list')


def is_name(val):
    return val[0] == '`'
##    return \
##           val not in BUILTIN_OPS and\
##           val not in BLOCKS and\
##           val not in LISTS and\
##           not is_str(val) and\
##           not is_num(val) and\
##           not is_bool(val)


def is_var(val):
        return \
            val not in BUILTIN_OPS and\
            val not in BLOCKS and\
            val not in LISTS and\
            not is_str(val) and\
            not is_num(val) and\
            not is_bool(val) and\
            not is_name(val)
