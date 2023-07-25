import copy
import threading
import time

from parse_exp import parse_exp, compute_exp
import xmindparser
from neo4jClass import Neo4jOperation


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


def detective_bool(F: dict, S: dict, fun_list: list):
    for single_fun in fun_list:
        if compute_exp(F, S, single_fun):
            continue
        else:
            return False
    return True


class RelationGenerate:
    def __init__(self, neo4j: Neo4jOperation, xmind_detached):
        self.neo4j = neo4j
        self.detached = xmind_detached
        self.record_list = list()
        self.runFlag = 1  # 1: run 2: pause 3: exit
        self.callBack = None
        self.t: threading.Thread = None

    def generate_mathcher(self, detach_list: list):
        """

        :param detach_list: xmind_dict[0]["detached"]
        :return:
        """
        relation_list = copy.deepcopy(detach_list)
        for single_relation in relation_list:
            for single_condition in single_relation["condition_list"]:

                condition_fun_list: list = list()  # expression convert to function list
                for single_exp in single_condition["expression_list"]:
                    exp_f = parse_exp(single_exp)
                    condition_fun_list.append(exp_f)
                single_condition["fun_list"] = condition_fun_list
                single_condition.pop("expression_list")

        return relation_list

    def generate_relation_instance(self, neo4j: Neo4jOperation, relation_list: list):
        """
        :param neo4j: the instance of Neo4jOperation
        :param relation_list: xmind_dict[0]["detached"]
        :return:
        """
        for single_relation in relation_list:
            node_label_f = single_relation["title_pair"][0]
            node_label_s = single_relation["title_pair"][1]

            node_of_f = neo4j.find_node_by_label(node_label_f)
            node_of_s = neo4j.find_node_by_label(node_label_s)
            for f in node_of_f:
                for s in node_of_s:
                    for single_condition in single_relation["condition_list"]:
                        relation_title = single_condition["relation_title"]
                        fun_list = single_condition["fun_list"]
                        if detective_bool(f, s, fun_list):
                            rn = neo4j.cr_relation(f, relation_title, s)

                            self.record_list.append(rn)
                            self.callBack(rn)

                            if self.runFlag == 1:
                                pass
                            elif self.runFlag == 2:
                                while self.runFlag == 2:
                                    time.sleep(1)
                            elif self.runFlag == 3:
                                return

                        else:
                            continue

    def run(self):
        relation_list = self.generate_mathcher(self.detached)

        self.t = threading.Thread(target=self.generate_relation_instance, args=(self.neo4j, relation_list))
        self.t.start()

    def pause(self):
        self.runFlag = 2

    def resume(self):
        self.runFlag = 1

    def stop(self):
        self.runFlag = 3
        self.t.join()
        self.t = None

    def setCallBack(self, callBack):
        self.callBack = callBack

    def goBack(self):
        for r in self.record_list:
            self.neo4j.delete(r)


if __name__ == '__main__':
    xmind_dict = xmindparser.xmind_to_dict("../source/x2.xmind")  # get xmind_dict
    xmind_content = xmind_dict[0]["topic"]  # get xmind_content which content which include all table and field

    db_name: str = xmind_content["title"]  # get db_name : database name
    db_table: list = xmind_content["topics"]  # get db_table : database tables

    detached_list = xmind_dict[0]["detached"]  # get detached_list : the list of relation between tables

    # relation_list = generate_mathcher(detached_list)
    # generate_relation_instance(Neo4jOperation(), relation_list)  # just for illustration
