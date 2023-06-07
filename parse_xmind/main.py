import copy
from parse_exp import parse_exp

import xmindparser


def parse_table_sheet(db_table):
    """
    :param db_table: xmind_dict[0]["topic"]["topics"]
    :return: {table_name:field_lis,table_name2:field_lis2} field_lis:[{title:name,tp:type}]
    """
    table_dic = dict()
    for table in db_table:
        tb_name = table["title"]
        field_iter = table["topics"]
        field_lis = list()
        for field in field_iter:
            title = field["title"]
            tp = field["topics"][0]["title"]
            field_lis.append({"title": title, "tp": tp})
        table_dic[tb_name] = field_lis
    return table_dic


def generate_mathcher(detach_list: list):
    back_dict = copy.deepcopy(detach_list)
    for single_relation in back_dict:
        for single_condition in single_relation["condition_list"]:

            condition_fun_list: list = list()
            for single_exp in single_condition["expression_list"]:
                exp_f = parse_exp(single_exp)
                condition_fun_list.append(exp_f)
            single_condition["expression_list"] = condition_fun_list

    return back_dict


if __name__ == '__main__':
    xmind_dict = xmindparser.xmind_to_dict("../source/x2.xmind")  # get xmind_dict
    xmind_content = xmind_dict[0]["topic"]  # get xmind_content which content which include all table and field

    db_name: str = xmind_content["title"]  # get db_name : database name
    db_table: list = xmind_content["topics"]  # get db_table : database tables

    detached_list = xmind_dict[0]["detached"]  # get detached_list : the list of relation between tables

    matcher = generate_mathcher(detached_list)
