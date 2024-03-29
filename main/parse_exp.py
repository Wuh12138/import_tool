import operator


def is_sym(char: str):
    sy = ['+', '-', '=', '*', '/', '(', ')', '{', '}', '<', '>', ">=", "<="]
    for i in sy:
        if char == i:
            return True
    else:
        return False


def is_number(string):
    if "." in string:
        parts = string.split(".")
        if len(parts) != 2:
            return False
        return parts[0].isdigit() and parts[1].isdigit()
    else:
        return string.isdigit()


def add_va(va: str, docker: list):
    """
    将列表元素的类型用type标识
    type:: 0:symbol 1:field 2:number 3:str
    :param va:
    :param docker:
    :return:
    """
    if va == '':
        return
    elif is_number(va):
        docker.append({"type": 2, "value": va})

    elif '.' in va:
        docker.append({"type": 1, "value": va})
    elif va[0] == '\"':
        docker.append({"type": 3, "value": va})
    else:
        raise TypeError(f"error:invalid identify : '{va}' ")


def parse_expression(exp: str):
    """
    将表达式转换为列表，标识了元素的type
    parse expression to list
    :param exp:
    :return: expression list
    """
    ele_lis = list()
    ele_variable = str()

    i: int = 0
    while i < len(exp):

        if is_sym(exp[i]):
            t = exp[i]
            if is_sym(t + exp[i + 1]):  # notice the ">=" "<="
                t = t + exp[i + 1]
                i += 1

            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            ele_lis.append({"type": 0, "value": t})
            ele_variable = ''

        elif exp[i] == ' ':
            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            ele_variable = ''

        elif exp[i].isdigit() or exp[i].isalpha() or exp[i] == '.' or exp[i] == '_' or exp[i] == '\"':
            ele_variable += exp[i]
        else:
            raise AssertionError(f"error: invalid character : '{exp[i]}' ")
        i += 1
    add_va(ele_variable, ele_lis)
    return ele_lis


def sym_rank(sym: str):
    if sym in ['+', '-']:
        return 1
    elif sym in ['*', '/']:
        return 2
    elif sym == '(':
        return 4
    elif sym in ['<', '>', '{', '}', '=', ">=", "<="]:
        return 0
    elif sym == '#':
        return -1


def convert_exp_to_back(exp: list):
    """
    将单条逻辑表达式转换为后缀表达式
    convert expression to back expression
    :param exp:
    :return:
    """
    sy_stk: list = list()
    sy_stk.append({"type": 0, "value": '#'})  # avoid the empty stack
    evaluate_stk: list = list()
    for s in exp:

        if s["type"] == 0:
            if s["value"] == ')':  # solve the (,  )
                while sy_stk[-1]["value"] != '(':
                    evaluate_stk.append(sy_stk.pop())
                sy_stk.pop()

            elif sym_rank(s["value"]) < sym_rank(sy_stk[-1]["value"]) and sy_stk[-1]["value"] != '(':  # solve * / + -
                while sym_rank(sy_stk[-1]["value"]) >= sym_rank(s["value"]) and sy_stk[-1]["value"] != '(':
                    evaluate_stk.append(sy_stk.pop())
                sy_stk.append(s)

            else:  # directly add symbol
                sy_stk.append(s)

        else:  # add variable
            evaluate_stk.append(s)

    while sy_stk[-1]["value"] != '#':  # proceed the remain thing
        evaluate_stk.append(sy_stk.pop())
    return evaluate_stk


def left_contain(a,b):
    """
    判断a是否在b中，将in函数化，替换后缀表达式中的{符号
    :param a:
    :param b:
    :return:
    """
    if a in b:
        return True
    else:
        return False

def sym_to_fun(sym: str):
    """
    将后缀表达中的符号转化为相应的函数，以便直接计算
    :param sym:
    :return:
    """
    if sym == '+':
        return operator.add
    elif sym == '-':
        return operator.sub
    elif sym == '*':
        return operator.mul
    elif sym == '/':
        return operator.truediv
    elif sym == '=':
        return operator.eq
    elif sym == '>=':
        return operator.ge
    elif sym == "<=":
        return operator.le
    elif sym == '>':
        return operator.gt
    elif sym == '<':
        return operator.lt
    elif sym == '{':
        return operator.contains
    elif sym == '}':
        return left_contain

def exp_to_fun(back_exp: list):
    """
    将单条后缀表达式中的符号转换为与之等价的函数，以便直接计算,添加新的逻辑或算术运算符请在sym_to_fun中添加等价的函数
    :type:4 infer the element is a sign 忘记什么意思了，不要乱改
    :type:10 infer the param need to compute and storage in another list which for save compute result,the value is indexing
    :param back_exp:
    :return:
    """
    fun_list: list = list()
    additional_list_index = 0
    i = 0
    while len(back_exp) != 1:
        if back_exp[i]["type"] != 0:
            i += 1
        else:
            fun_list.append({"type": 4, "value": sym_to_fun(back_exp[i]["value"])})
            fun_list.append(back_exp[i - 2])
            fun_list.append(back_exp[i - 1])
            back_exp[i - 2] = {"type": 10, "value": additional_list_index}
            additional_list_index += 1
            back_exp.pop(i - 1)
            back_exp.pop(i - 1)
            i -= 1

    return fun_list


def convert_arguments(f: dict, s: dict, va: dict, tp_value: list):
    """
    将表达式中的变量转换为相应的值
    :param f:
    :param s:
    :param va:
    :param tp_value:
    :return:
    """
    if va["type"] == 1:
        l = va["value"].split('.')
        source_indentify = l[0]
        se = None
        if source_indentify == 'f':
            se = f
        elif source_indentify == 's':
            se = s
        else:
            raise AssertionError(f"error: unexpected indentify \"{va['value']}\" ")
        return se[l[1]]
    elif va["type"] == 2:
        return float(va["value"])
    elif va["type"] == 10:
        return tp_value[va["value"]]
    else:
        return va["value"]


def compute_exp(f: dict, s: dict, fun_list: list):
    """
    计算单条表达式的值
    :param f: the first table dict which is an instance
    :param s: the second table dict which is an instance
    :param fun_list:
    :return:
    """
    i = 0
    tp_value: list = list()
    while i < len(fun_list):
        if fun_list[i]["type"] == 4:
            fun = fun_list[i]["value"]
            ag1 = convert_arguments(f, s, fun_list[i + 1], tp_value)
            ag2 = convert_arguments(f, s, fun_list[i + 2], tp_value)
            tp_value.append(fun(ag1, ag2))
            i += 2
        else:
            i += 1

    return tp_value.pop()


def parse_exp(exp: str):
    """
    将原始表达式转化为计算之前的函数，变量表达式，将返回值做为参数调用compute_exp函数即可计算表达式的bool值
    :param exp:
    :return:
    """
    back_exp = convert_exp_to_back(parse_expression(exp))
    fun_lis = exp_to_fun(back_exp)
    return fun_lis


if __name__ == "__main__":
    test = "(f.field_1+s.field_1)*10/3-1>=100"

    test_data_1 = {
        "field_1": 10
    }

    test_data_2 = {
        "field_1": 20
    }

    back_exp = convert_exp_to_back(parse_expression(test))
    fun_lis = exp_to_fun(back_exp)
    r = compute_exp(test_data_1, test_data_2, fun_lis)
    print(r)
