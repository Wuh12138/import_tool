import xmindparser

xmind_dict = xmindparser.xmind_to_dict("../source/x2.xmind")

print(xmind_dict)

xmind_content = xmind_dict[0]["topic"]

db_name: str = xmind_content["title"]
db_table: list = xmind_content["topics"]




def parse_table_sheet(db_table):
    table_lis = list()
    for table in db_table:
        field_iter=table["topics"]
        field_list=list()
        for field in field_iter:
            field_list.append(field["title"])
        table_lis.append({"table_title":table["title"],"fields":field_list})
    return table_lis



title,dic=parse_table_sheet(db_table)



pass
