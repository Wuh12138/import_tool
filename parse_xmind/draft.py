test = "f.field_1+s.field_1=10"


def is_sym(char: str):
    sy = ['+', '-', '=', '*', '/', '(', ')', "{", "}"]
    for i in sy:
        if char == i:
            return True
    else:
        return False

def add_va(va:str,docker:list):
    if va=='':
        return
    elif va[0].isdigit():
        if va.isnumeric():
            docker.append({"type":2,"value":va})
        else:
            raise ValueError(f"error: the variable '{va}' is invalid")
    elif '.' in va:
        pass # TODO:




ele_lis = list()
ele_variable = str()
for i in range(len(test)):

    if is_sym(test[i]):
        # append back variable if it not ''
        if ele_variable != '':
            ele_lis.append(ele_variable)
        ele_lis.append(test[i])
        i += 1
        ele_variable = ''

    elif test[i] == ' ':
        # append back variable if it not ''
        if ele_variable != '':
            ele_lis.append(ele_variable)
        i += 1
        ele_variable = ''


