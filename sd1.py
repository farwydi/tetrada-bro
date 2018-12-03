import string

from tabulate import tabulate

# asd[123]
from lexer import make_parse, reg_parse
from poliz import poliz
from trans import to_trans


def get_4d(s):
    ss = s.split(';')

    for l in ss:
        if 'make(' in l:
            make_parse(l)
        else:
            return reg_parse(l)

    return []


def show(trans_):
    print(tabulate(trans_,
                   headers=['op', 'arg1', 'arg2', 'result']))


s = "make(x, 10, 10, 10, 10);~f{1, j+5*(6*2+1)}+x[4, j+5*(6*2+1), 8, y]^5"
# s = input("ex: ")
print(s)
print(tabulate(to_trans(poliz(get_4d(s))),
               headers=['op', 'arg1', 'arg2', 'result']))
