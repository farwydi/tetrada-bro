def poliz(smap):
    # ПОЛИЗ
    op_prior = {
        '#': 4,
        '~': 3,
        '^': 2,
        '*': 1,
        '/': 1,
        '+': 0,
        '-': 0,
    }
    normal_lex = []
    stack = []
    for lex in smap:
        if lex[0] is 9:
            # for ps in lex[1][1]:
            #     normal_lex += poliz(ps)
            # normal_lex.append((9, lex[1][0]))
            normal_lex.append(lex)
            continue
        if lex[0] is -1:
            continue
        if lex[0] in [0, 1]:
            normal_lex.append(lex)
        elif lex[0] == 10:  # (
            stack.append(lex)
        elif lex[0] == 11:  # )
            if 10 not in [x[0] for x in stack]:
                raise SyntaxError("Отсутствует открывающая скобка")
            while stack[-1][0] != 10:
                normal_lex.append(stack.pop())
            if stack[-1][0] != 10:
                raise SyntaxError("Отсутствует закрывающая скобка")
            else:
                stack.pop()
        else:
            while len(stack) > 0 and stack[-1][0] != 10 and op_prior[stack[-1][1]] >= op_prior[lex[1]]:
                normal_lex.append(stack.pop())
            stack.append(lex)
            continue

    while len(stack) > 0:
        if stack[-1][0] in [10, 11]:
            raise SyntaxError('Ошибка порядка скобок')
        normal_lex.append(stack.pop())

    # print(''.join([x[1] for x in normal_lex]))
    return normal_lex
