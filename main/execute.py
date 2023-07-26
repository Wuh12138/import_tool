from generate_node import MapFromSql
from generate_node import MapFromXlsx
from neo4jClass import Neo4jOperation
import parse_xmind
import xmindparser
import threading


class Execute:
    def __init__(self):
        self.content = None
        self.detached = None
        self.neo4j: Neo4jOperation = None
        self.source = None
        self.rn_generator: parse_xmind.RelationGenerate = None

        self.stepFlag = 0

    def parse_xmind(self, xmind_path: str):

        xmind = xmindparser.xmind_to_dict(xmind_path)
        self.content = xmind[0]["topic"]
        self.detached = xmind[0]["detached"]

        self.rn_generator = parse_xmind.RelationGenerate(self.neo4j, self.detached)

    def __execute(self):
        self.stepFlag = 1
        self.source.map()
        self.source.t.join()
        print("node import finished")
        self.stepFlag = 2
        self.generate_relation()
        self.rn_generator.t.join()
        print("relation import finished")
        self.stepFlag = 3

    def execute(self):
        t = threading.Thread(target=self.__execute)
        t.start()

    def generate_relation(self):
        self.rn_generator.run()

    def set_neo4j(self, key, name="neo4j", url='http://localhost:7474'):
        try:
            self.neo4j = Neo4jOperation(key=key, name=name, url=url)
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

    def pause(self):
        if self.stepFlag == 0:
            pass
        elif self.stepFlag == 1:
            self.source.pause()
        elif self.stepFlag == 2:
            self.rn_generator.pause()

    def resume(self):
        if self.stepFlag == 0:
            pass
        elif self.stepFlag == 1:
            self.source.resume()
        elif self.stepFlag == 2:
            self.rn_generator.resume()

    def stop(self):
        if self.stepFlag == 0:
            pass
        elif self.stepFlag == 1:
            self.source.stop()
        elif self.stepFlag == 2:
            self.rn_generator.stop()

    def __goBack(self):
        if self.stepFlag == 0:
            pass
        elif self.stepFlag == 1:
            self.source.goBack()
        elif self.stepFlag == 3:
            self.stepFlag = 2
            self.rn_generator.goBack()
            self.rn_generator.t.join()
            self.stepFlag = 1
            self.source.goBack()

        self.stepFlag = 0

    def goBack(self):
        t = threading.Thread(target=self.__goBack)
        t.start()

    def s_pause(self):
        self.source.pause()

    def s_resume(self):
        self.source.resume()

    def s_stop(self):
        self.source.stop()

    def s_setCallBack(self, callBack):
        self.source.setCallBack(callBack)

    def s_goBack(self):
        self.source.goBack()

    def r_pause(self):
        self.rn_generator.pause()

    def r_resume(self):
        self.rn_generator.resume()

    def r_stop(self):
        self.rn_generator.stop()

    def r_setCallBack(self, callBack):
        self.rn_generator.setCallBack(callBack)

    def r_goBack(self):
        self.rn_generator.goBack()
