from poliz import poliz

i = 0
var_i = 0

def to_trans(nmap, r='return'):
    global i, var_i
    stack = []
    trans = []
    for lex in nmap:
        if lex[0] == 9:
            for a in lex[1][1]:
                trans += to_trans(poliz(a), 'push')
            trans.append((i, lex[1][0], "", "", f"${var_i}"))
            stack.append((-1, f"${var_i}"))
            i += 1
            var_i += 1
        elif lex[0] in [1, 0]:
            if len(lex) == 2:
                stack.append(lex)
        else:
            if lex[0] in [3, 9]:
                trans.append((i, lex[1], stack.pop()[1], "", f"${var_i}"))
            else:
                a = stack.pop()[1]
                b = stack.pop()[1]
                trans.append((i, lex[1], b, a, f"${var_i}"))
            stack.append((-1, f"${var_i}"))
            i += 1
            var_i += 1
    while len(stack) > 0:
        a = stack.pop()[1]
        trans.append((i, r, a, "", ""))
        i += 1
    return trans
