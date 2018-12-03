from poliz import poliz


def to_trans(nmap, r='return', i=0, var_i=0):
    stack = []
    trans = []
    for lex in nmap:
        if lex[0] == 9:
            for a in lex[1][1]:
                trans_b, i, var_ix = to_trans(poliz(a), 'push', i, var_i)
                trans += trans_b
            trans.append((i, "argx", len(lex[1][1]), "", ""))
            i += 1
            trans.append((i, "call", lex[1][0], "", f"${var_i}"))
            stack.append((-1, f"${var_i}"))
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
    return trans, i, var_i
