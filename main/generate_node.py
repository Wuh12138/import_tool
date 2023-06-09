from neo4jClass import Neo4jOperation
from sqlClass import SqlOperation


class MapFromSql:
    def __init__(self, xmind_content: dict, neo4j: Neo4jOperation, **param):
        """

        :param xmind_content: xmind[0]["topic"]
        :param sql:
        :param neo4j:
        """
        self.sql = SqlOperation(param['host'], param['user'], param['password'], param['database'])
        self.neo4j = neo4j
        self.xmind_content = xmind_content

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
        self.xmind_content = xmind_content

    def map(self):
        pass
