test = "(f.field_1+s.field_1)*3+55*32=100"


def is_sym(char: str):
    sy = ['+', '-', '=', '*', '/', '(', ')', '{', '}', '<', '>']
    for i in sy:
        if char == i:
            return True
    else:
        return False


def add_va(va: str, docker: list):
    """
    0:symbol 1:field 2:number 3:str
    :param va:
    :param docker:
    :return:
    """
    if va == '':
        return
    elif va[0].isdigit():
        if va.isnumeric():
            docker.append({"type": 2, "value": va})
        else:
            raise ValueError(f"error: the variable '{va}' is invalid")
    elif '.' in va:
        docker.append({"type": 1, "value": va})
    elif va[0] == '\"':
        docker.append({"type": 3, "value": va})
    else:
        raise TypeError(f"error:invalid identify : '{va}' ")


def parse_expression(exp: str):
    ele_lis = list()
    ele_variable = str()
    for i in range(len(exp)):

        if is_sym(exp[i]):
            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            ele_lis.append({"type": 0, "value": exp[i]})
            ele_variable = ''

        elif exp[i] == ' ':
            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            ele_variable = ''

        elif exp[i].isdigit() or exp[i].isalpha() or exp[i] == '.' or exp[i] == '_' or exp[i] == '\"':
            ele_variable += exp[i]
        else:
            raise AssertionError(f"error: invalid character : '{exp[i]}' ")
    add_va(ele_variable, ele_lis)
    return ele_lis


def sym_rank(sym: str):
    if sym in ['+', '-']:
        return 1
    elif sym in ['*', '/']:
        return 2
    elif sym == '(':
        return 4
    elif sym in ['<', '>', '{', '}', '=']:
        return 0
    elif sym == '#':
        return -1


def convert_exp(exp: list):
    evaluate_stk: list = list()
    sy_stk: list = list()
    sy_stk.append('#')  # avoid the empty stack
    evaluate_stk: list = list()
    for s in exp:

        if s["type"] == 0:
            if s["value"] == ')':  # solve the (,  )
                while sy_stk[-1] != '(':
                    evaluate_stk.append(sy_stk.pop())
                sy_stk.pop()

            elif sym_rank(s["value"]) < sym_rank(sy_stk[-1]) and sy_stk[-1] != '(':  # solve * / + -
                while sym_rank(sy_stk[-1]) >= sym_rank(s["value"]) and sy_stk[-1] != '(':
                    evaluate_stk.append(sy_stk.pop())
                sy_stk.append(s["value"])

            else:  # directly add symbol
                sy_stk.append(s["value"])

        else:  # add variable
            evaluate_stk.append(s)

    while sy_stk[-1] != '#':  # proceed the remain thing
        evaluate_stk.append(sy_stk.pop())
    return evaluate_stk


t1 = parse_expression(test)

back_exp = convert_exp(t1)

pass
