import xmindparser

xmind_dict = xmindparser.xmind_to_dict("../source/x2.xmind")

print(xmind_dict)

xmind_content = xmind_dict[0]["topic"]

db_name: str = xmind_content["title"]
db_table: list = xmind_content["topics"]


def parse_table_sheet(db_table):
    """

    :param db_table:
    :return: {table_name:field_lis,table_name2:field_lis2} field_lis:[{title:name,tp:type}]
    """
    table_dic=dict()
    for table in db_table:
        tb_name = table["title"]
        field_iter = table["topics"]
        field_lis = list()
        for field in field_iter:
            title = field["title"]
            tp = field["topics"][0]["title"]
            field_lis.append({"title": title, "tp": tp})
        table_dic[tb_name]=field_lis
    return table_dic


parse_table_sheet(db_table)
pass
