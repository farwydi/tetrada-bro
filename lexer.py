import string

var_map = {}


# asd       0
# 123       1
# ~         3
# +         4
# -         5
# *         6
# /         7
# ^         8
# func      9
# (         10
# )         11
# push      12
#           13
# arr       14

def make_parse(s):
    s = s[5:]
    if not s[-1] is ')':
        raise SyntaxError(f"Ошибка в конструкции make")
    s = s[:-1]
    if s[0] in string.digits:
        raise SyntaxError(f"Ошибка в конструкции make ожидается переменная")
    i = s.find(',')
    if i == -1:
        raise SyntaxError(f"Ошибка в конструкции make не задан масив")
    var = s[0:i]
    shape = [x.strip(' ') for x in s[i + 1:].split(',')]
    var_map[var] = shape


def reg_parse(s):
    lexer_map = []

    op_map = '~+-*/^()'
    cell_func_liter = 'cell'

    def add_arr(ar, of):
        ar_body = var_map[ar]
        dop = ''

        for k in range(len(of)):
            dop += "+" + of[k]
            for l in range(k, len(of) - 1):
                dop += "*" + ar_body[l]
        dop = dop[1:]

        # for z in range(len(of) - 1):
        #     if dop == '':
        #         dop += f"({of[z]}*{ar_body[z + 1]}+{of[z + 1]})"
        #         continue
        #     dop = f"({dop}*{of[z]}*{ar_body[z + 1]}+{of[z + 1]})"
        # dop = dop[1:]
        # for _ in range(len(of) - 1):
        #     dop += ')'

        lm = [(10, '(')] + reg_parse(dop) + [(11, ')')]
        return lm

    def op_detect(op):
        if op == "~":
            return 3
        if op == "(":
            return 10
        if op == ")":
            return 11
        if op == cell_func_liter:
            return 9
        p = op_map.index(op)
        if p != -1:
            return p + 3

    buf = ''
    state = 0
    func = []
    arr = []
    ofsset = []
    argv = []
    for i, l in enumerate(s):
        if l is ' ':
            continue

        if state == 0:
            if l in string.ascii_letters:
                state = 1
                buf += l
                continue

            if l in string.digits:
                state = 2
                buf += l
                continue

            if l in op_map:
                if l is '~':
                    lexer_map.append((-1, '0'))
                    lexer_map.append((3, l))
                else:
                    lexer_map.append((op_detect(l), l))
        elif state == 1:
            # Переменная
            if l in string.ascii_letters + string.digits:
                buf += l
                continue

            if l is '[':
                state = 5
                arr = buf
                if arr not in [x[0] for x in var_map]:
                    raise SyntaxError(f"Массив не обявлен")
                buf = ''
                continue

            if l is '{':
                # func
                state = 4
                func = buf
                buf = ''
                continue

            if l in op_map:
                lexer_map.append((0, buf))
                if l is '~':
                    lexer_map.append((-1, '0'))
                    lexer_map.append((3, l))
                else:
                    lexer_map.append((op_detect(l), l))
                buf = ''
                state = 0
        elif state == 2:
            # Константа
            if l in string.ascii_letters:
                raise SyntaxError("Переменная не может начинатся с цифр")

            if l in string.digits:
                buf += l
                continue

            if l is '[':
                raise SyntaxError("Константа не  может быть массивом")

            if l is '(':
                raise SyntaxError("константа не может быть функцией")

            if l in op_map:
                lexer_map.append((1, buf))
                if l is '~':
                    lexer_map.append((-1, '0'))
                    lexer_map.append((3, l))
                else:
                    lexer_map.append((op_detect(l), l))
                buf = ''
                state = 0
        elif state == 4:
            # argv func
            if l is '}':
                state = 0
                if buf != '':
                    argv.append(buf)
                    buf = ''
                if len(argv) > 0:
                    argv = [reg_parse(x) for x in argv]
                    lexer_map.append((9, (func, argv)))
                    argv = []
                else:
                    lexer_map.append((9, (func, [])))
                continue

            if l is ',':
                argv.append(buf)
                buf = ''
                continue

            if l in string.ascii_letters + string.digits + op_map:
                buf += l
                continue
        elif state == 5:
            if l is ']':
                state = 0
                ofsset.append(buf)
                buf = ''
                if len(var_map[arr]) != len(ofsset):
                    raise SyntaxError("Не верный вызов масива")
                lexer_map.append((1, arr))
                lexer_map.append((14, '#'))
                lexer_map += add_arr(arr, ofsset)
                continue

            if l is ',':
                ofsset.append(buf)
                buf = ''
                continue

            if l in string.ascii_letters + string.digits + op_map:
                buf += l
                continue

    if state == 1:
        lexer_map.append((0, buf))
    elif state == 2:
        lexer_map.append((1, buf))

    # print([x[1] for x in lexer_map])
    return lexer_map
    # normal_lex = poliz(lexer_map)
    # t_lex = to_trans(normal_lex)
