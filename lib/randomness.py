# Note this file isn't named "random" - if it were, it would not let me
# import Python's builtin random module!

import random


def _random(interpeter, stack, scopes, stream):
    tok = interpeter.Token(
        TYPE='num', VAL=random.randint(0, 1000000) / 1000000.0)
    stack.append(tok)

module = {
    "random": _random
}
