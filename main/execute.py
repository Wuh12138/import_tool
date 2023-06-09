from generate_node import MapFromSql
from generate_node import MapFromXlsx
from neo4jClass import Neo4jOperation
import parse_xmind
import xmindparser


class Execute:
    def __init__(self):
        self.content = None
        self.detached = None
        self.neo4j: Neo4jOperation = None
        self.source = None

    def set_xmind_path(self, xmind_path: str):
        xmind = xmindparser.xmind_to_dict(xmind_path)
        self.content = xmind[0]["topic"]
        self.detached = xmind[0]["detached"]

    def execute(self):
        pass
        self.source.map()
        print("node import finished")
        self.generate_relation()
        print("relation import finished")

    def generate_relation(self):
        relation_list = parse_xmind.generate_mathcher(self.detached)
        parse_xmind.generate_relation_instance(self.neo4j, relation_list)

    def set_neo4j(self, key, name="neo4j", url='http://localhost:7474'):
        try:
            self.neo4j = Neo4jOperation(key, name, url)
            return [True]
        except Exception as e:
            return [False, e]

    def set_source(self, *db_type: str, **param):
        if db_type[0] == "mysql":
            self.source = MapFromSql(self.content, self.neo4j, **param)
        elif db_type[0] == "xlsx":
            self.source = MapFromXlsx(self.content, self.neo4j, **param)
        else:
            raise Exception("db_type must be sql or xlsx")
