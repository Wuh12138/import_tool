test = "f.field_1+s.field_1=10"


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
    elif va.isalnum():
        docker.append({"type": 3, "value": va})
    else:
        raise TypeError(f"error:invalid identify : '{va}' ")


def parse_expression(exp: str):
    ele_lis = list()
    ele_variable = str()
    for i in range(len(test)):

        if is_sym(test[i]):
            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            ele_lis.append({"type": 0, "value": test[i]})
            i += 1
            ele_variable = ''

        elif test[i] == ' ':
            # append back variable if it not ''
            add_va(ele_variable, ele_lis)
            i += 1
            ele_variable = ''

        elif test[i].isdigit() or test.isalpha():
            ele_variable += test[i]
            i += 1
        else:
            raise AssertionError(f"error: invalid character : '{test[i]}' ")
    return ele_lis


def convert_exp(exp: list):
    pass
