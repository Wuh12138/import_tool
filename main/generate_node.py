from neo4jClass import Neo4jOperation
from sqlClass import SqlOperation
import parse_xmind
import xlrd
import openpyxl


class MapFromSql:
    def __init__(self, xmind_content: dict, neo4j: Neo4jOperation, **param):
        """

        :param xmind_content: xmind[0]["topic"]
        :param sql:
        :param neo4j:
        """
        self.sql = SqlOperation(param['host'], param['user'], param['password'], param['database'])
        self.neo4j = neo4j
        self.db_name = xmind_content['title']
        self.relation_dic = parse_xmind.parse_table_sheet(xmind_content['topics'])

    def map(self):
        pass

    def transit(self):
        sql_database = self.xmind_content['title']
        mp = self.sql
        np = self.neo4j
        """节点实体建立"""
        mp.execute_query(f'use {sql_database};')
        # all name of tables in database,as label in neo4j
        tables = mp.table_list()
        # database import
        for table_name in tables:
            # TODO:
            neo4j_lable = table_name
            sql_statement = mp.query_statements(table_name)
            records = mp.execute_query(sql_statement)

            # one table import
            for record in records:
                structs = mp.table_struct(table_name)
                record_index = 0
                dic = {}

                # import one record
                for struct in structs:
                    # special type process
                    type_name = struct[1]
                    dic_value = mp.tranform_source(type_name, record[record_index])
                    dic[struct[0]] = dic_value
                    record_index = record_index + 1

                try:
                    no = np.node(neo4j_lable, **dic)
                    np.cr_node(no)
                except:
                    np.delete_all()
                    print('error: ' + table_name)
                    print(dic)
                    exit(1)
            print(table_name)


class MapFromXlsx:
    def __init__(self, xmind_content: dict, neo4j: Neo4jOperation, **param):
        self.neo4j = neo4j
        self.db_name = xmind_content['title']
        self.relation_dic = parse_xmind.parse_table_sheet(xmind_content['topics'])
        self.xlsx_path = param['xlsx_path']

    @staticmethod
    def check_field(column_name: str, field_lis: list):
        for single_filed in field_lis:
            if column_name == single_filed["title"]:
                return [True, single_filed["tp"]]
        return [False]

    def column_type(self, column_name_list: list, field_lis: list):
        columns_type = list()
        for column_name in column_name_list:
            check_result = self.check_field(column_name, field_lis)
            if check_result[0]:
                columns_type.append(check_result[1])
            else:
                raise AssertionError(f"column name {column_name} not in xmind")

        return columns_type

    @staticmethod
    def type_convert(type: str, value):
        if type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "str":
            return value
        else:
            raise AssertionError(f"type {type} not support")

    @staticmethod
    def row_cell(row_value):
        r = list()
        for c in row_value:
            r.append(c.value)
        return r

    def map(self):
        work_book = openpyxl.load_workbook(self.xlsx_path)
        sheet_name_list = work_book.sheetnames
        for sheet_name in sheet_name_list:
            if sheet_name not in self.relation_dic.keys():  # check if sheet name in xmind
                raise AssertionError(f"sheet name {sheet_name} not in xmind")

            sheet = work_book.get_sheet_by_name(sheet_name)
            # get all column name
            rows_list = list(sheet.rows)
            column_name_list:list = MapFromXlsx.row_cell(rows_list[0])
            columns_type = self.column_type(column_name_list, self.relation_dic[sheet_name])

            label_cache: list = list()
            for i in range(1, len(rows_list)):
                row = MapFromXlsx.row_cell(rows_list[i])
                single_label_instance: dict = dict()
                for j in range(len(column_name_list)):
                    single_label_instance[column_name_list[j]] = MapFromXlsx.type_convert(columns_type[j], row[j])
                label_cache.append(single_label_instance)
            for label in label_cache:
                try:
                    no = self.neo4j.node(sheet_name, **label)
                    self.neo4j.cr_node(no)
                except Exception as e:
                    print(e)
                    print(label)
                    exit(1)
