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


# s = "make(x, 10, 10);asd{1,h}^x[1,g+4]"
# s = "make(x, 10);x[5]"
s = "f{1,x}"
s = "f{1}"
s = "f{1}+f{x}"
s = "f{1}+f{x}+f{}+f{1, 2, 3, 4}"
s = "(1+2)*4+3"
s = "a+b+c"
# s = "f{}"
# s = "x+2*y*(4+z)"
# s = "~x^(5+3)"
# s = "make(x, 15, 20, 40);x[1,g+4,8]"
# 8+40*((g+4)+20*(1+15))
# (i+10)*20+j
# s = "make(x, 10, 10, 10, 10);~f{1, j+5*(6*2+1)}+x[4, j+5*(6*2+1), 8, y]^5"
# s = "make(x, 10, 15);x[7,8]" # 7*15+8
# s = "make(x, 10, 15, 25);x[7,8,5]"
s = "make(x, n, m, l);x[i,j,k]"
# s = input("ex: ")
print(s)
x, _, _ = to_trans(poliz(get_4d(s)))
print(tabulate(x[:-1],
               headers=['op', 'arg1', 'arg2', 'result']))
