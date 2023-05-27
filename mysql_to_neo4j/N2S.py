from neo4jClass import Neo4jOperation
from sqlClass import SqlOperation


class N2S:
    """"""
    def __init__(self, np: Neo4jOperation, mp: SqlOperation, sql_database: str):
        if type(np)!=Neo4jOperation and type(mp)!=SqlOperation:
            print("type error in N2S Class")
        self.__np=np
        self.__mp=mp
        self.__sql_database=sql_database

    def transit(self):
        sql_database=self.__sql_database
        mp=self.__mp
        np=self.__np
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
        """关系实体建立"""
        relations = mp.get_relation_model(sql_database)
        for relation in relations:
            group_lable = np.match_node(relation[3])  # 通过主键所在表的标签进行查找
            for source_node in group_lable:
                source_field = relation[4]
                target_label = relation[0]  # 外键所在表的label
                target_field = relation[1]
                relation_lable = relation[2]
                dic = {}
                dic[target_field] = source_node[source_field]
                target_nodes = np.match_node(target_label, **dic)
                for target_node in target_nodes:
                    np.cr_relation(source_node, target_node, FOREIGN_KEY=relation_lable)
            print(relation)



if __name__=='__main__':
    np =Neo4jOperation(key="12345678")
    mp =SqlOperation(host='localhost', user='root', password='123456',database='sakila')
    n2s = N2S(np=np, mp=mp, sql_database='sakila')

    #n2s.transit()
