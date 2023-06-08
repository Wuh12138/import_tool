import pymysql
from shapely.wkb import loads  # process geometry


class SqlOperation:
    """
    MySQL 数据库操作类
    """

    def __init__(self, host, user, password, database):
        """
        构造函数，创建数据库连接和游标
        """
        self.db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8mb4')
        self.cursor = self.db.cursor()

    def execute_query(self, sql):
        """
        执行 SQL 查询语句并返回查询结果
        """
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def execute_update(self, sql):
        """
        执行 SQL 更新语句并提交更改
        """
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        """
        关闭游标和数据库连接
        """
        self.cursor.close()
        self.db.close()

    def table_struct(self, table_name):
        """
        :param table_name: 表名
        :return: 返回形式是 ( (Field, Type, NullKey, Default, Extra）, ('''), ('''))
        """
        return self.execute_query(f'desc {table_name};')

    def table_list(self):
        """
        :return: 返回数据库中的所有表格的名称的list
        """
        table_list = self.execute_query('show tables;')
        ls = []
        for i in table_list:
            ls.append(i[0])
        return ls

    def get_value(self, field, table_name):
        """

        :param field:属性
        :param table_name: 目标表名
        :return: 返回改属性所有值的list[(value1,),(value2,)]
        """
        return self.execute_query(f'select {field} from {table_name};')

    def record_touple(self, table_name):
        """

        :param table_name: 表名
        :return: 返回
        """
        return self.execute_query(f'select * from {table_name};')

    def tranform_source(self, type_name:str, source):
        """

        :param type_name:
        :param source:
        :return:
        """
        match_name=type_name.split('(')[0]
        if source is None:
            return 'null'
        match match_name:
            case 'data':# TODO:
                return source.strftime('%Y-%m-%d %H:%M:%S')
            case 'time':# TODO:
                return source.strftime('%Y-%m-%d %H:%M:%S')
            case 'datetime':# TODO:
                return source.strftime('%Y-%m-%d %H:%M:%S')
            case 'timestamp':# TODO: convert to data
                return source.strftime('%Y-%m-%d %H:%M:%S')
            case 'geometry':# TODO: convert to point
                return str(loads(source))
            case 'decimal':
                return float(source)
            case 'blob':#TODO:
                return 'error'

            # TO add
            case _:
                return source




    def query_statements(self, table_name):
        statement = 'select '
        structs = self.table_struct(table_name)
        temp_statement=''
        for struct in structs:

            match struct[1]:
                case 'geometry':
                    temp_statement= f'ST_AsBinary({struct[0]})'
                case 'blob':
                    temp_statement=f'{struct[0]}'
                case _:
                    temp_statement= f'{struct[0]}'
            flag=' ' in struct[0]
            if flag:
                temp_statement='`'+temp_statement+'`,'
            else:
                temp_statement=temp_statement+','
            statement=statement+temp_statement

        statement= statement.strip(',')
        statement = statement + f' from {table_name};'
        return statement

    def get_relation_model(self,database_name):
        """
        :param database_name: 数据库名称
        :return: (('address', 'city_id', 'fk_address_city', 'city', 'city_id'),('''),),外键表名，外键列名，外键名称，主键表名，主键列名
        """
        sql = f'''
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                CONSTRAINT_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                TABLE_SCHEMA = '{database_name}' AND
                REFERENCED_TABLE_NAME IS NOT NULL;
        '''
        return self.execute_query(sql)
